from typing import Optional

import disnake
from disnake import WebhookMessage

from services.database.message_db import add_message, retrieve_message_to_reply
from services.portal.webhook import Webhook


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
        return self

    async def send(self, msg: disnake.Message, original_message_id: int = None):
        """
        Send a message to the channel.
        If a discord message is passed, the bot will try to imitate the message and author using a webhook.
        A MessageLike can be passed for finer control.
        """
        if msg.channel == self.channel:
            return

        # Handle if this message is replying to another message
        reply_notif = None
        try:
            if not original_message_id is None:
                message_to_reply_id = await retrieve_message_to_reply(original_message_id, self.hook.channel.id)
                message_to_reply = await self.channel.fetch_message(int(message_to_reply_id))
                reply_notif = await message_to_reply.reply(content=f"{msg.author.name}'s message below is replying to this message. [Test](https://google.com/)")
        except:
            print("Couldn't find the message to reply to")

        files = [await attc.to_file() for attc in msg.attachments]
        webhook_message: WebhookMessage = await self.hook.send(content=msg.content,
                                                               avatar_url=str(msg.author.avatar.url),
                                                               username=msg.author.name, tts=msg.tts,
                                                               files=files, wait=True)
        await add_message(original_message_id=msg.id, copy_message_id=webhook_message.id,
                          channel_id=webhook_message.channel.id)
        if reply_notif is not None:
            embed = disnake.Embed(description=f"[Jump to message]({webhook_message.jump_url})")
            await reply_notif.edit(embed=embed, content="")