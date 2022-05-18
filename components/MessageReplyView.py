import disnake


class MessageReplyView(disnake.ui.View):
    message: disnake.Message

    def __init__(self, message: disnake.Message, copy_message: disnake.Message):
        super().__init__()
        self.message = message
        self.add_item(
            disnake.ui.Button(style=disnake.ButtonStyle.blurple,
                              label=f"Replying to {copy_message.author.name}",
                              disabled=True))
        message_content = message.reference.cached_message.content
        if len(message_content) == 0:
            message_preview = "[No message preview]"
        elif len(message_content) <= 50:
            message_preview = message_content
        else:
            message_preview = f"{message_content[:50]}..."
        self.add_item(
            disnake.ui.Button(style=disnake.ButtonStyle.link,
                              label=message_preview,
                              url=copy_message.jump_url))
