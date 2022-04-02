import collections
from typing import Dict
import disnake
from tenacity import stop_after_attempt, retry, wait_fixed

from models.database.channel import Channel
from models.database.portal import Portal
from services.database.driver import driver_service, commit_session
from services.portal.chain import Chain


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
def load_channels(bot) -> Dict[int, int]:
    channels = driver_service.session.query(Channel)
    channels_dict = {}
    for channel in channels:
        channels_dict[int(channel.channel_id)] = int(channel.portal_id)
    return channels_dict


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
async def load_portals(bot) -> Dict[int, Chain]:
    portals = driver_service.session.query(Portal)
    channels = driver_service.session.query(Channel)
    portals_dict = collections.defaultdict(Chain)
    channels_dict: Dict[int, list[disnake.TextChannel]] = collections.defaultdict(list[disnake.TextChannel])
    for channel in channels:
        if not channels_dict.get(int(channel.portal_id)):
            channels_dict[int(channel.portal_id)] = []
        channels_dict[int(channel.portal_id)].append(bot.get_channel(int(channel.channel_id)))
    for portal in portals:
        if not portals_dict.get(int(portal.portal_id)):
            portals_dict[int(portal.portal_id)] = await Chain.new(channels_dict[int(portal.portal_id)])
    return portals_dict


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
async def add_portal(portal_id: int, channel_id: int):
    driver_service.session.add(Portal(portal_id=portal_id, primary_channel_id=channel_id))
    commit_session()


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
async def add_channel(portal_id: int, channel_id: int):
    driver_service.session.add(Channel(portal_id=portal_id, channel_id=channel_id))
    commit_session()


@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
async def remove_channel(channel_id: int):
    result = driver_service.session.query(Channel).filter_by(channel_id=channel_id).one()
    driver_service.session.delete(result)
    commit_session()
