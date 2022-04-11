import disnake
from disnake import TextChannel

from utilities import embed


class Webhook:

    @staticmethod
    async def connect(channel: TextChannel, name: str):
        """
        Returns a webhook object for the given channel and name.
        If the webhook does not exist, it will be created.
        """
        try:
            hooks = await channel.webhooks()
            for hook in hooks:
                if hook.name == name:
                    return hook
            else:
                return await channel.create_webhook(name=name)
        except disnake.errors.Forbidden as err:
            await channel.send(embed=embed.error_embed("Missing Manage Webhooks permissions", err.text))
            return None
