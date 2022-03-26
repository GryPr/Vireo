import types
import disnake


class MessageLike:
    """
    Children of this class may be passed to Link.send for complete control over the message sent by the webhook
    """
    content: str
    tts: bool
    id: int
    author: types.SimpleNamespace

    def __init__(self, content, author_name="unset", author_avatar_url="unset", tts: bool = False, msg_id: int = None,
                 channel: disnake.TextChannel = None, attachments=None, reference=None):
        """
        Customize your own message. Use this when you aren't simply echoing a message.
        """
        if attachments is None: attachments = []
        self.attachments = attachments
        self.content = content
        self.tts = tts
        self.id = msg_id
        self.channel = channel
        self.reference = reference
        self.author = types.SimpleNamespace(name=author_name, avatar_url=author_avatar_url)

    @classmethod
    def from_message(cls, msg: disnake.Message):
        """
        Create a MessageLike from a discord.Message.
        """
        if isinstance(msg, cls):
            return msg
        else:
            return cls(
                content=msg.content,
                author_name=msg.author.name,
                author_avatar_url=msg.author.avatar_url,
                tts=msg.tts,
                id=msg.id,
                channel=msg.channel,
                attachments=msg.attachments,
                reference=msg.reference
            )