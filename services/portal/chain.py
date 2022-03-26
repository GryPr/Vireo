import disnake
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
        if message.channel in (link.channel for link in self.links):
            for link in self.links:
                await link.send(message)