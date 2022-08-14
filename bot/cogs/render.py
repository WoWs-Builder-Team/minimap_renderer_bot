import nextcord
import asyncio

from io import BytesIO
from utils.connection import REDIS, ASYNC_REDIS
from utils.exceptions import ReplayParsingError, ReplayRenderingError
from rq import Queue
from rq.job import Job
from rq.worker import Worker
from tasks.single import render_single
from nextcord.ext import commands
from nextcord import (
    Attachment,
    Interaction,
    SlashOption,
    File,
    Embed,
)

QUEUE = Queue(name="single", connection=REDIS)

ORANGE = 0xFF9933
RED = 0xFF0000
YELLOW = 0xFFFF00
GREEN = 0x00FF00


def track_task_request(f):
    async def wrapped(
        cls,
        ia: Interaction,
        attachment: Attachment,
        *args,
        **kwargs,
    ):
        user = ia.user
        assert user
        await ASYNC_REDIS.set(f"task_request_{user.id}", "", ex=180)
        try:
            return await f(cls, ia, attachment, *args, **kwargs)
        except Exception:
            pass
        finally:
            await ASYNC_REDIS.delete(f"task_request_{user.id}")

    return wrapped


def check(f):
    async def wrapped(
        cls,
        ia: Interaction,
        attachment: Attachment,
        *args,
        **kwargs,
    ):
        user = ia.user
        assert user

        worker_count = Worker.count(queue=QUEUE)
        cooldown = await ASYNC_REDIS.ttl(f"cooldown_{user.id}")

        try:
            assert QUEUE.count <= 10, "Queue full!"
            assert worker_count != 0, "No running workers!"
            assert cooldown <= 0, "You're on cooldown!"
            assert not await ASYNC_REDIS.exists(
                f"task_request_{user.id}"
            ), "You already have an ongoing render!"
        except AssertionError as e:
            await ia.send(e.args[0])
        else:
            return await f(cls, ia, attachment, *args, **kwargs)

    return wrapped


class EmbedProducer:
    def __init__(self, attachment: Attachment) -> None:
        self._attachment = attachment

    def get_embed(self, color: int = ORANGE, **kwargs) -> Embed:
        embed = Embed(title="Minimap Renderer", color=color)

        embed.add_field(
            name="File", value=self._attachment.filename, inline=False
        )

        if description := kwargs.get("description"):
            embed.description = description

        if error := kwargs.get("error"):
            embed.add_field(name="Error", value=error)

        if status := kwargs.get("status"):
            embed.add_field(name="Status", value=status)

        if progress := kwargs.get("progress"):
            progress = round(10 * progress)
            embed.add_field(
                name="Progress",
                value=f"{'▮' * progress}{'▯' * (10 - progress)}",
            )

        return embed


class CogRender(commands.Cog):
    def __init__(self, bot: commands.Bot | commands.AutoShardedBot) -> None:
        self._bot = bot

    @check
    @track_task_request
    async def _poll_result(
        self,
        ia: Interaction,
        attachment: Attachment,
        fps: int,
        quality: int,
        logs: bool,
        chat: bool,
        anonymous: bool,
    ):
        ep = EmbedProducer(attachment)
        replay_bytes = await attachment.read()
        job_ttl = max(QUEUE.count, 1) * 300

        job: Job = QUEUE.enqueue(
            render_single,
            kwargs={
                "user_id": ia.user.id,  # type: ignore
                "replay_bytes": replay_bytes,
                "fps": fps,
                "quality": quality,
                "logs": logs,
                "chat": chat,
                "anonymous": anonymous,
            },
            failure_ttl=180,
            result_ttl=180,
            ttl=job_ttl,
        )

        embed = ep.get_embed(ORANGE, description="Replay Received!")
        msg = await ia.send(embed=embed)

        while True:
            # queued, started, failed, finished
            status = job.get_status(refresh=True)
            match status:
                case "queued":
                    embed = ep.get_embed(ORANGE, status="Queued")
                    await msg.edit(embed=embed)
                case "started":
                    meta = job.get_meta(refresh=True)
                    if progress := meta.get("progress", None):
                        embed = ep.get_embed(
                            YELLOW,
                            progress=progress,
                            status="Rendering",
                        )
                    elif task_status := meta.get("status", None):
                        embed = ep.get_embed(YELLOW, status=task_status)
                    else:
                        embed = ep.get_embed(YELLOW, status="Started")
                    await msg.edit(embed=embed)
                case "finished":
                    if isinstance(job.result, bytes):
                        try:
                            embed = ep.get_embed(GREEN, status="Completed")
                            with BytesIO(job.result) as video_data:
                                file = File(video_data, "minimap.mp4")
                                await msg.edit(embed=embed)
                                await ia.send(file=file)
                        except nextcord.HTTPException:
                            embed = ep.get_embed(
                                RED,
                                error="Rendered file is too large (>8MB). "
                                "Consider reducing the render quality",
                            )
                        except Exception as e:
                            embed = ep.get_embed(RED, error="Unknown error.")
                    elif isinstance(job.result, ReplayParsingError):
                        embed = ep.get_embed(
                            RED, error="Replay parsing error."
                        )
                    elif isinstance(job.result, ReplayRenderingError):
                        embed = ep.get_embed(
                            RED, error="Replay rendering error."
                        )
                    else:
                        embed = ep.get_embed(RED, error="Unknown error.")
                    await msg.edit(embed=embed)
                    break
                case "failed":
                    embed = ep.get_embed(RED, error="Unknown error.")
                    await msg.edit(embed=embed)
                    break
                case _:
                    embed = ep.get_embed(RED, error="Render task expired.")
                    await msg.edit(embed=embed)
            await asyncio.sleep(1)

    @nextcord.slash_command(description="Renders your replay file.")
    async def render(
        self,
        interaction: Interaction,
        attachment: Attachment = SlashOption(
            description="Your World of Warships replay file.",
            required=True,
        ),
        fps: int = SlashOption(
            description="Render fps. Default: 30",
            required=False,
            default=30,
            min_value=20,
            max_value=30,
        ),
        quality: int = SlashOption(
            description="Render quality. Default: 7",
            required=False,
            default=7,
            min_value=1,
            max_value=9,
        ),
        logs: bool = SlashOption(
            description="Enables logs. Default: True",
            required=False,
            default=True,
        ),
        chat: bool = SlashOption(
            description="Displays chat logs. Ignored when logs is False."
            " Default: True",
            required=False,
            default=True,
        ),
        anonymous: bool = SlashOption(
            description="Anonymizes the usernames. Ignored when logs is False."
            "Default: False",
            required=False,
            default=False,
        ),
    ):
        await interaction.response.defer(with_message=True)
        loop = asyncio.get_running_loop()
        loop.create_task(
            self._poll_result(
                ia=interaction,
                attachment=attachment,
                fps=fps,
                quality=quality,
                logs=logs,
                chat=chat,
                anonymous=anonymous,
            )
        )
