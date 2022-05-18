import disnake
from components.MessageReplyView import MessageReplyView
from disnake import RawMessageUpdateEvent, WebhookMessage
from disnake.utils import MISSING
from services.database.message_db import add_message, retrieve_message_to_reply
from services.portal.webhook import Webhook
from utilities.filter import censor_message


class Link:
    """A class that bundles a webhook and a channel. Multiple "links" combine to form a "chain"."""
    hook: disnake.Webhook
    channel: disnake.TextChannel

    @classmethod
    async def new(cls, channel: disnake.TextChannel):
        """Create a new Link object."""
        self = cls()
        self.channel = channel
        self.hook = await Webhook.connect(channel, "Vireo")
        return self

    async def update(self, message_to_update: disnake.Message,
                     updated_message: RawMessageUpdateEvent):
        await self.hook.edit_message(message_to_update.id,
                                     content=updated_message.data["content"])

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
        webhook_message: WebhookMessage = await self.hook.send(
            content=censor_message(message.content),
            avatar_url=str(message.author.avatar.url),
            username=f"{message.author.name} from {message.guild.name}",
            tts=message.tts,
            files=files,
            wait=True,
            view=view)
        # Add message to database
        await add_message(original_message_id=message.id,
                          copy_message_id=webhook_message.id,
                          channel_id=webhook_message.channel.id)
