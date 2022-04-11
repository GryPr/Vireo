import disnake
from disnake import WebhookMessage, RawMessageUpdateEvent
from disnake.utils import MISSING
from tenacity import stop_after_attempt, retry

from components.MessageReplyView import MessageReplyView
from services.database.message_db import add_message, retrieve_message_to_reply
from services.portal.webhook import Webhook
from utilities.filter import filter_words


class Link:
    """
    A class that bundles a webhook and a channel. Multiple "links" combine to form a "chain".
    """
    hook: disnake.Webhook
    channel: disnake.TextChannel

    @classmethod
    async def new(cls, channel: disnake.TextChannel):
        """
        Create a new Link object.
        """
        self = cls()
        self.channel = channel
        self.hook = await Webhook.connect(channel, "Vireo")
        if not self.hook:
            return None
        return self

    async def update(self, message_to_update_id: int,
                     updated_message: RawMessageUpdateEvent):
        if message_to_update_id == updated_message.message_id:
            return
        try:
            await self.hook.edit_message(message_to_update_id,
                                         content=updated_message.data["content"])
        except disnake.errors.NotFound:
            print("Did not find message to update")

    async def delete(self, message_to_delete: disnake.Message):
        await self.hook.delete_message(message_to_delete.id)

    @retry(stop=stop_after_attempt(2))
    async def send(self,
                   message: disnake.Message,
                   reply_message_id: int = None):
        """
        Send a message to the channel.
        If a discord message is passed, the bot will try to imitate the message and author using a webhook.
        A MessageLike can be passed for finer control.
        """
        if message.channel == self.channel:
            return

        # Handle if this message is replying to another message
        view = MISSING
        try:
            if reply_message_id is not None:
                message_to_reply_id = await retrieve_message_to_reply(
                    reply_message_id, self.hook.channel.id)
                message_to_reply = await self.channel.fetch_message(
                    int(message_to_reply_id))
                view = MessageReplyView(message, message_to_reply)
        except Exception as e:
            print(f"Couldn't find the message to reply to - {e}")

        # Send webhook message
        files = [await attc.to_file() for attc in message.attachments]
        try:
            webhook_message: WebhookMessage = await self.hook.send(
                content=filter_words(message.content),
                avatar_url=str(message.author.avatar.url),
                username=f"{message.author.name} from {message.guild.name}",
                tts=message.tts,
                files=files,
                wait=True,
                view=view)
        except disnake.errors.NotFound:
            self.hook = await Webhook.connect(self.channel, "Vireo")
            raise Exception
        # Add message to database
        await add_message(original_message_id=message.id,
                          copy_message_id=webhook_message.id,
                          channel_id=webhook_message.channel.id)
