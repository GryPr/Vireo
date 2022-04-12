import disnake.ui


class MessageReplyView(disnake.ui.View):
    message: disnake.Message

    def __init__(self, message: disnake.Message, copy_message: disnake.Message):
        super().__init__()
        self.message = message
        self.add_item(
            disnake.ui.Button(style=disnake.ButtonStyle.blurple,
                              label=f"Replying to {copy_message.author.name}",
                              disabled=True))
        if len(message.reference.cached_message.content) <= 0:
            message_preview = "[No message preview]"
        elif len(message.reference.cached_message.content) <= 50:
            message_preview = f"{message.reference.cached_message.content}"
        else:
            message_preview = f"{self.message.reference.cached_message.content[:50]}..."
        self.add_item(
            disnake.ui.Button(style=disnake.ButtonStyle.link,
                              label=message_preview,
                              url=f"{copy_message.jump_url}"))
