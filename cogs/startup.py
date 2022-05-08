import os
import platform
import random
from typing import Sequence

import disnake
import services.portal.transmission as Transmission
from disnake.ext import commands, tasks
from disnake.ext.commands import Bot


class Startup(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @tasks.loop(minutes=1.0)
    async def display_statuses(self, *, statuses: Sequence[str]) -> None:
        """
        Randomly set the game status of the bot.

        :param statuses: the statuses to randomly choose from
        """
        status = random.choice(statuses)
        await self.bot.change_presence(activity=disnake.Game(status))

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Called when the bot is ready."""
        print(f"Logged in as {self.bot.user.name}")
        print(f"disnake API version: {disnake.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(
            f"Running on: {platform.system()} {platform.release()} ({os.name})")
        print("-------------------")

        self.display_statuses.start(
            statuses=["with you!", "with Krypton!", "with humans!"])

        await Transmission.transmission_service.initialize(self.bot)


def setup(bot: Bot):
    bot.add_cog(Startup(bot))
    print(f"> Extension {__name__} is ready\n")
