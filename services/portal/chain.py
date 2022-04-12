import asyncio
import collections
from typing import Dict

import disnake

from services.database.message_db import retrieve_original_message, add_message
from services.portal.link import Link


class Chain:
    links: Dict[int, Link]
    """
    A class that wraps a list of Links. Represent a single connected network of channels, which echo back to each other.
    """

    @classmethod
    async def new(cls, channels: list[disnake.TextChannel]):
        """
        Create a new Link object.
        """
        self = cls()
        self.links = collections.defaultdict(Link)
        for ch in channels:
            if not ch:
                continue
            self.links[ch.id] = await Link.new(ch)
        return self

    async def add(self, channel: disnake.TextChannel):
        self.links[channel.id] = await Link.new(channel)

    async def remove(self, id: int):
        del self.links[id]

    async def send(self, message: disnake.Message):
        """
        If the message is sent to a link/channel in the chain, it will be sent to all the links in the chain.
        """

        # If the message is a reply, grab the original message ID
        original_message_id = None
        if message.reference is not None:
            try:
                original_message_id = await retrieve_original_message(
                    message.reference.message_id)
            except:
                print("Couldn't find the message to reply to")

        await add_message(message.id, message.id, message.channel.id)
        if message.channel in (link.channel for link in self.links.values()):
            await asyncio.gather(*[
                link.send(message, reply_message_id=original_message_id)
                for link in self.links.values()
            ])
