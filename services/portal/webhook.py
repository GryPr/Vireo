import disnake


class Webhook:

    @staticmethod
    async def connect(channel: disnake.TextChannel,
                      name: str) -> disnake.Webhook:
        """
        Return a webhook object for the given channel and name.
        If the webhook does not exist, create it.
        """
        hooks = await channel.webhooks()
        for hook in hooks:
            if hook.name == name:
                return hook
        return await channel.create_webhook(name=name)
