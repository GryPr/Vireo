class Webhook:

    @staticmethod
    async def connect(channel, name):
        """
        Returns a webhook object for the given channel and name.
        If the webhook does not exist, it will be created.
        """
        hooks = await channel.webhooks()
        for hook in hooks:
            if hook.name == name:
                return hook
        else:
            return await channel.create_webhook(name=name)
