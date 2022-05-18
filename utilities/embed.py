import disnake


def generic_embed(title: str, description: str, author: str) -> disnake.Embed:
    embed = disnake.Embed(color=0x09a2e3)
    embed.title = title
    embed.description = description
    embed.set_footer(text=f"Requested by {author}")
    return embed


def wip_embed() -> disnake.Embed:
    embed = disnake.Embed(title="You're early!",
                          description="Command has not been implemented yet!")
    return embed


def error_embed(error: str, title: str = "Error has occurred") -> disnake.Embed:
    embed = disnake.Embed(color=0xff0000)
    embed.title = title
    embed.description = error
    return embed
