from sqlalchemy.exc import PendingRollbackError, OperationalError
from tenacity import stop_after_attempt, retry, wait_exponential

from models.database.message import Message
from services.database.driver import driver_service, commit_session


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
async def add_message(original_message_id: int, copy_message_id: int, channel_id: int):
    driver_service.session.add(
        Message(original_message_id=str(original_message_id), copy_message_id=copy_message_id, channel_id=channel_id))
    commit_session()


# Retrieve the copy message that is linked to an original message ID
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
async def retrieve_copy_message(original_message_id: int, channel_id: int):
    result = driver_service.session.query(Message).filter_by(original_message_id=str(original_message_id),
                                                             channel_id=str(channel_id)).one()
    return result


# Retrieve original message ID to fetch all messages linked to the original
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
async def retrieve_original_message(copy_message_id: int) -> int:
    result = driver_service.session.query(Message).filter_by(copy_message_id=str(copy_message_id)).one()
    return int(result.original_message_id)


# Retrieve message specific to channel
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
async def retrieve_message_to_reply(original_message_id: int, channel_id: int) -> int:
    message_to_reply: Message = await retrieve_copy_message(original_message_id, channel_id)
    return message_to_reply.copy_message_id


# Retrieves messages filtered by original message ID
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=5))
async def retrieve_copy_messages(original_message_id: int) -> list[Message]:
    try:
        result = driver_service.session.query(Message).filter_by(original_message_id=str(original_message_id)).all()
    except OperationalError:
        raise Exception
    except Exception as e:
        print(e)
        raise Exception
    return result
