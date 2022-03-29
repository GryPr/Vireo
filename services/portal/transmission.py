import asyncio

import disnake
from typing import Dict, List

from disnake import RawMessageDeleteEvent, RawMessageUpdateEvent
from disnake.ext.commands import Bot

import utilities.random
from models.database.message import Message
from services.database.message_db import retrieve_copy_messages
from services.database.portal_db import load_channels, load_portals, add_portal, add_channel
from services.portal.chain import Chain
from services.portal.link import Link


class Transmission:
    channels: Dict[int, int]  # key=channel_id, value=portal_id
    portals: Dict[int, Chain]

    async def initialize(self, bot: Bot):
        self.channels = load_channels(bot)
        self.portals = await load_portals(bot)

    async def add_channel_to_portal(self, channel: disnake.TextChannel, portal_id: int):
        await self.portals[portal_id].add(channel.id, await Link.new(channel))
        self.channels[channel.id] = portal_id
        await add_channel(portal_id, channel.id)

    async def add_portal(self, primary_channel: disnake.TextChannel) -> int:
        portal_id = utilities.random.generate_random_int()
        self.portals[portal_id] = await Chain.new([primary_channel])
        await add_portal(portal_id, primary_channel.id)
        return portal_id

    def portal_id_exists(self, portal_id: int) -> bool:
        if not self.portals[portal_id]:
            return False
        else:
            return True

    def channel_in_portal(self, channel_id: int) -> bool:
        if self.channels is None:
            return False
        if not self.channels.get(channel_id):
            return False
        else:
            return True

    async def handle_message(self, message: disnake.Message):
        if self.channels is None:
            return
        portal_id: int = self.channels.get(message.channel.id)
        if not portal_id:
            return
        chain: Chain = self.portals[portal_id]
        await chain.send(message)

    async def handle_update(self, updated_message: RawMessageUpdateEvent, bot: Bot):
        original_message = bot.get_message(updated_message.message_id)
        if updated_message.data["content"] is None:
            return
        copy_messages_db: List[Message] = await retrieve_copy_messages(original_message.id)
        copy_messages: List[disnake.Message] = []
        for copy_message in copy_messages_db:
            message = bot.get_message(copy_message.copy_message_id)
            if message.author.bot:
                copy_messages.append(message)
        await asyncio.gather(
            *[self.portals[self.channels[copy_message.channel.id]].links[copy_message.channel.id]
                  .update(copy_message, updated_message) for copy_message in copy_messages])

    async def handle_delete(self, payload: RawMessageDeleteEvent, bot: Bot):
        copy_messages_db: List[Message] = await retrieve_copy_messages(payload.message_id)
        copy_messages: List[disnake.Message] = []
        for copy_message in copy_messages_db:
            message = bot.get_message(copy_message.copy_message_id)
            if not message:
                continue
            copy_messages.append(message)
        await asyncio.gather(
            *[copy_message.delete() for copy_message in copy_messages])


transmission_service = Transmission()
