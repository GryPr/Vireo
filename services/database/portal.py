from typing import Dict, List
import disnake

from models.database.channel import Channel
from models.database.portal import Portal
from services.database.driver import driver_service
from services.portal.chain import Chain


def load_channels(bot) -> Dict[int, int]:
    channels = Channel.query.all()
    channels_dict = {}
    for channel in channels:
        channels_dict[channel.channel_id] = channel.portal_id
    return channels_dict


async def load_portals(bot) -> Dict[int, Chain]:
    portals = Portal.query.all()
    channels = Channel.query.all()
    portals_dict = {}
    channels_dict: Dict[int, List[disnake.TextChannel]] = {}
    for channel in channels:
        if not channels_dict[channel.portal_id]:
            channels_dict[channel.portal_id] = []
        channels_dict[channel.portal_id].append(bot.get_channel(channel))
    for portal in portals:
        if not portals_dict[portal.portal_id]:
            portals_dict[portal.portal_id] = await Chain.new(channels[portal.portal_id])
    return portals_dict


async def add_portal(portal_id: int, channel_id: int):
    driver_service.session.add(Portal(portal_id=portal_id, primary_channel_id=channel_id))
    await add_channel(portal_id, channel_id)


async def add_channel(portal_id: int, channel_id: int):
    driver_service.session.add(Channel(portal_id=portal_id, channel_id=channel_id))
