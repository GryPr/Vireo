import services.portal.transmission as Transmission
from disnake import Message, RawMessageDeleteEvent, RawMessageUpdateEvent
from disnake.ext import commands
from disnake.ext.commands import Bot


class Message(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        """
        Called when someone sends a message, with or without the bot prefix
        :param message: The message that was sent
        """
        if message.author == self.bot.user or message.author.bot:
            return
        await Transmission.transmission_service.handle_message(message)
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_raw_message_delete(self,
                                    payload: RawMessageDeleteEvent) -> None:
        """
        Called when a message is deleted
        :param payload: The raw event payload data
        """
        if not Transmission.transmission_service.channel_in_portal(
                payload.channel_id):
            return
        await Transmission.transmission_service.handle_delete(payload, self.bot)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: RawMessageUpdateEvent) -> None:
        """
        Called when a message is edited
        :param payload: the raw event payload data
        """
        if not Transmission.transmission_service.channel_in_portal(
                payload.channel_id):
            return
        await Transmission.transmission_service.handle_update(payload, self.bot)


def setup(bot: Bot):
    bot.add_cog(Message(bot))
    print(f"> Extension {__name__} is ready\n")
