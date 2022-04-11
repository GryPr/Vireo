import disnake
from disnake import Embed


def generic_embed(title: str, description: str, author: str) -> Embed:
    embed = disnake.Embed(color=0x09a2e3)
    embed.title = title
    embed.description = description
    embed.set_footer(text=f"Requested by {author}")
    return embed


def wip_embed() -> Embed:
    embed = disnake.Embed(title="You're early!",
                          description=f"Command has not been implemented yet!")
    return embed


def error_embed(error: str, title: str = "Error has occurred") -> Embed:
    embed = disnake.Embed(color=0xff0000)
    embed.title = title
    embed.description = error
    return embed
