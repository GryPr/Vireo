import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot

from services.portal.transmission import transmission_service
from utilities.embed import wip_embed, error_embed


class Portal(commands.Cog, name="portal"):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.transmission = transmission_service

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description="Manage a portal")
    async def portal(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @portal.sub_command(description="Create a new portal")
    async def initialize(self, inter: disnake.ApplicationCommandInteraction):
        portal_id: int = await transmission_service.add_portal(inter.channel)
        embed = disnake.Embed(title="New portal created", description=f"Portal ID: {portal_id}")
        embed.add_field(
            name="Subscribe other servers using this command",
            value=f"/portal sub {portal_id}",
            inline=False
        )
        await inter.send(embed=embed)

    @portal.sub_command(description="Subscribe the channel to a portal")
    async def sub(self, inter: disnake.ApplicationCommandInteraction, portal_id: int):
        # try:
        await transmission_service.add_channel_to_portal(inter.channel, portal_id)
        # except Exception as e:
        #     print(e)
        #     await inter.send(embed=error_embed("Error has occured adding the channel to the portal"))
        #     return
        embed = disnake.Embed(title="Added channel to the portal", description=f"Portal ID: {portal_id}")
        embed.add_field(
            name="Subscribe other servers using this command",
            value=f"/portal sub {portal_id}",
            inline=False
        )
        await inter.send(embed=embed)

    @portal.sub_command(description="Wipe all portals")
    async def wipe(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send(embed=wip_embed())

    @portal.sub_command(description="List all portals")
    async def list(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send(embed=wip_embed())

    @portal.sub_command(description="Kick a subscriber")
    async def kick(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send(embed=wip_embed())

    @portal.sub_command(description="Regenerate the portal ID")
    async def regenerate(self, inter: disnake.ApplicationCommandInteraction):
        await inter.send(embed=wip_embed())


def setup(bot):
    bot.add_cog(Portal(bot))
    print(f"> Extension {__name__} is ready\n")
