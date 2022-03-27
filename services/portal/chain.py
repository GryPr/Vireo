import disnake

from services.database.message_db import retrieve_original_message, add_message
from services.portal.link import Link


class Chain:
    """
    A class that wraps a list of Links. Represent a single connected network of channels, which echo back to each other.
    """
    @classmethod
    async def new(cls, channels):
        """
        Create a new Link object.
        """
        self = cls()
        self.links = [await Link.new(ch) for ch in channels]
        return self

    async def add(self, channel: disnake.TextChannel):
        self.links.append(await Link.new(channel))

    async def send(self, message: disnake.Message):
        """
        If the message is sent to a link/channel in the chain, it will be sent to all the links in the chain.
        """

        # If the message is a reply, grab the original message ID
        original_message_id = None
        if not message.reference is None:
            try:
                original_message_id = await retrieve_original_message(message.reference.message_id)
            except:
                print("Couldn't find the message to reply to")

        await add_message(message.id, message.id, message.channel.id)
        if message.channel in (link.channel for link in self.links):
            for link in self.links:
                await link.send(message, original_message_id=original_message_id)