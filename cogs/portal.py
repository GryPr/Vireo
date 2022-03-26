import disnake
from disnake.ext import commands

from services.portal.transmission import transmission_service


class Portal(commands.Cog, name="portal"):
    def __init__(self, bot):
        self.bot = bot
        self.transmission = transmission_service

    @commands.has_permissions(admin=True)
    @commands.slash_command(description="Manage a portal")
    async def portal(self):
        pass

    @portal.sub_command()
    async def new(self):
        print("WIP")

    @portal.sub_command()
    async def sub(self):
        print("WIP")

    @portal.sub_command()
    async def wipe(self):
        print("WIP")

    @portal.sub_command()
    async def list(self):
        print("WIP")

    @portal.sub_command()
    async def kick(self):
        print("WIP")

    @portal.sub_command()
    async def regenerate(self):
        print("WIP")


def setup(bot):
    bot.add_cog(Portal(bot))
