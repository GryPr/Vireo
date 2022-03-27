import disnake
from typing import Dict

import services.database.portal_db
import utilities.random
from services.database.message_db import add_message
from services.database.portal_db import load_channels, load_portals, add_portal, add_channel
from services.portal.chain import Chain
from services.portal.link import Link


class Transmission:
    channels: Dict[int, int]
    portals: Dict[int, Chain]

    async def initialize(self, bot):
        self.channels = load_channels(bot)
        self.portals = await load_portals(bot)

    async def add_channel_to_portal(self, channel: disnake.TextChannel, portal_id: int):
        self.portals[portal_id].links.append(await Link.new(channel))
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
        if not self.channels[channel_id]:
            return False
        else:
            return True

    async def handle_message(self, message: disnake.Message):
        portal_id: int = self.channels.get(message.channel.id)
        if not portal_id:
            return
        chain: Chain = self.portals[portal_id]
        await chain.send(message)

    async def handle_message_delete(self, message: disnake.Message):
        return

    async def handle_message_update(self, message: disnake.Message):
        return


transmission_service = Transmission()
