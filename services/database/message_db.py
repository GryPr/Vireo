from disnake import MessageType
from sqlalchemy import select
from sqlalchemy.orm import Query

from models.database.message import Message
from services.database.driver import driver_service


async def add_message(original_message_id: int, copy_message_id: int, channel_id: int):
    driver_service.session.add(
        Message(original_message_id=str(original_message_id), copy_message_id=copy_message_id, channel_id=channel_id))
    driver_service.session.commit()


# Retrieve the copy message that is linked to an original message ID
async def retrieve_copy_message(original_message_id: int, channel_id: int):
    result = driver_service.session.query(Message).filter_by(original_message_id=str(original_message_id), channel_id=str(channel_id)).one()
    return result


# Retrieve original message ID to fetch all messages linked to the original
async def retrieve_original_message(copy_message_id: int) -> int:
    result = driver_service.session.query(Message).filter_by(copy_message_id=str(copy_message_id)).one()
    return int(result.original_message_id)


# Retrieve message specific to channel
async def retrieve_message_to_reply(original_message_id: int, channel_id: int) -> int:
    message_to_reply: Message = await retrieve_copy_message(original_message_id, channel_id)
    return message_to_reply.copy_message_id
