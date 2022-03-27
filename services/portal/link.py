import disnake
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

    async def send(self, msg: disnake.Message):
        """
        Send a message to the channel.
        If a discord message is passed, the bot will try to imitate the message and author using a webhook.
        A MessageLike can be passed for finer control.
        """
        if msg.channel == self.channel:
            return
        files = [await attc.to_file() for attc in msg.attachments]

        await self.hook.send(content=msg.content, avatar_url=str(msg.author.avatar.url),
                             username=msg.author.name, tts=msg.tts, files=files)
