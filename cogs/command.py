import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import Bot
from exceptions import UserBlacklisted


class Command(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command(
            self, interaction: ApplicationCommandInteraction) -> None:
        """
        Called when a slash command has been successfully executed
        :param interaction: The slash command that has been executed
        """
        print(f"Executed {interaction.data.name} command "
              f"in {interaction.guild.name} (ID: {interaction.guild.id}) "
              f"by {interaction.author} (ID: {interaction.author.id})")

    @commands.Cog.listener()
    async def on_slash_command_error(self,
                                     interaction: ApplicationCommandInteraction,
                                     error: Exception) -> None:
        """
        Called when a valid slash command catches an error
        :param interaction: The slash command that failed executing
        :param error: The error that has been faced
        """
        if isinstance(error, UserBlacklisted):
            """
            The code here will only execute if the error is an instance of 'UserBlacklisted', which can occur when using
            the @checks.is_owner() check in your command, or you can raise the error by yourself.

            'hidden=True' will make so that only the user who execute the command can see the message
            """
            embed = disnake.Embed(
                title="Error!",
                description="You are blacklisted from using the bot.",
                color=0xE02B2B)
            print("A blacklisted user tried to execute a command.")
            return await interaction.send(embed=embed, ephemeral=True)
        elif isinstance(error, commands.errors.MissingPermissions):
            embed = disnake.Embed(
                title="Error!",
                description="You are missing the permission(s) `" +
                ", ".join(error.missing_permissions) +
                "` to execute this command!",
                color=0xE02B2B)
            print("A blacklisted user tried to execute a command.")
            return await interaction.send(embed=embed, ephemeral=True)
        raise error

    @commands.Cog.listener()
    async def on_command_completion(self, context: commands.Context) -> None:
        """
        Called when a normal command has been successfully executed
        :param context: The context of the command that has been executed
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        print(f"Executed {executed_command} command "
              f"in {context.guild.name} (ID: {context.message.guild.id}) "
              f"by {context.message.author} (ID: {context.message.author.id})")

    @commands.Cog.listener()
    async def on_command_error(self, context: commands.Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error
        :param context: The normal command that failed executing
        :param error: The error that has been faced
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = disnake.Embed(
                title="Hey, please slow down!",
                description=
                (f"You can use this command again in "
                 f"{f'{round(hours)} hours' if round(hours) > 0 else ''} "
                 f"{f'{round(minutes)} minutes' if round(minutes) > 0 else ''} "
                 f"{f'{round(seconds)} seconds' if round(seconds) > 0 else ''}."
                ),
                color=0xE02B2B)
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(
                title="Error!",
                description="You are missing the permission(s) `" +
                ", ".join(error.missing_permissions) +
                "` to execute this command!",
                color=0xE02B2B)
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = disnake.Embed(
                title="Error!",
                description=str(error).capitalize(),
                # We need to capitalize because the command arguments have no capital letter in the code.
                color=0xE02B2B)
            await context.send(embed=embed)
        raise error


def setup(bot: Bot):
    bot.add_cog(Command(bot))
    print(f"> Extension {__name__} is ready\n")
