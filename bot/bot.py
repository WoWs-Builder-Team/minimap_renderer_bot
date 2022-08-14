import os
import logging

from nextcord.ext import commands

from utils.environ import check_environment_var
from utils.logging import LOGGER_BOT
from .cogs.render import CogRender

logging.basicConfig(level=logging.DEBUG)


check_environment_var(["DISCORD_TOKEN"])

BOT = commands.Bot(help_command=None)
BOT.add_cog(CogRender(BOT))


@BOT.event
async def on_ready():
    print(f"Logged in as {BOT.user} (ID: {BOT.user.id})")  # type: ignore


def run():
    token = os.getenv("DISCORD_TOKEN")
    BOT.run(token=token)
