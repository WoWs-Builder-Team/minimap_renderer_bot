from io import BytesIO
from rq import get_current_job
from rq.job import Job
from replay_parser import ReplayParser
from renderer.data import ReplayData
from renderer.render import Renderer
from tempfile import NamedTemporaryFile
from utils.exceptions import ReplayParsingError, ReplayRenderingError
from utils.connection import REDIS


def render_single(
    user_id: int,
    replay_bytes: bytes,
    fps: int,
    quality: int,
    logs: bool,
    chat: bool,
    anonymous: bool,
):
    job: Job = get_current_job()  # type: ignore
    job.meta["status"] = "Reading"
    job.save_meta()
    try:
        try:
            with BytesIO(replay_bytes) as bio:
                replay_data: ReplayData = ReplayParser(
                    bio, strict=True
                ).get_info()["hidden"]["replay_data"]
        except Exception as e:
            raise ReplayParsingError from e
        else:
            job.meta["status"] = "Rendering"
            job.save_meta()

            def progress_cb(per: float):
                job.meta["progress"] = per
                job.save_meta()

            try:
                renderer = Renderer(replay_data, logs, anonymous, chat)
                with NamedTemporaryFile(suffix=".mp4") as tmp:
                    renderer.start(
                        tmp.name, fps, quality, progress_cb=progress_cb
                    )
                    tmp.seek(0)
                    return tmp.read(), renderer.get_player_build()
            except Exception as e:
                raise ReplayRenderingError from e
    except Exception as e:
        return e
    finally:
        REDIS.set(f"cooldown_{user_id}", "", ex=60)
