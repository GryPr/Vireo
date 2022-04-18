import os
import platform
import random
from typing import Sequence

import disnake
import exceptions
import services.portal.transmission as Transmission
from disnake import (ApplicationCommandInteraction, Message,
                     RawMessageDeleteEvent, RawMessageUpdateEvent)
from disnake.ext import commands, tasks
from disnake.ext.commands import Bot


class Startup(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @tasks.loop(minutes=1.0)
    async def display_statuses(self, *, statuses: Sequence[str]) -> None:
        """Randomly set the game status of the bot.

        :param statuses: the statuses to randomly choose from
        """
        status = random.choice(statuses)
        await self.bot.change_presence(activity=disnake.Game(status))

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Called when the bot is ready."""
        print(f"Logged in as {self.bot.user.name}")
        print(f"disnake API version: {disnake.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(
            f"Running on: {platform.system()} {platform.release()} ({os.name})")
        print("-------------------")

        self.display_statuses.start(
            statuses=["with you!", "with Krypton!", "with humans!"])

        await Transmission.transmission_service.initialize(self.bot)

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        """
        Called when someone sends a message, with or without the bot prefix
        :param message: The message that was sent
        """
        if message.author == self.bot.user or message.author.bot:
            return
        await Transmission.transmission_service.handle_message(message)
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_raw_message_delete(self,
                                    payload: RawMessageDeleteEvent) -> None:
        """
        Called when a message is deleted
        :param payload: The raw event payload data
        """
        if not Transmission.transmission_service.channel_in_portal(
                payload.channel_id):
            return
        await Transmission.transmission_service.handle_delete(payload, self.bot)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: RawMessageUpdateEvent) -> None:
        """
        Called when a message is edited
        :param payload: the raw event payload data
        """
        if not Transmission.transmission_service.channel_in_portal(
                payload.channel_id):
            return
        await Transmission.transmission_service.handle_update(payload, self.bot)

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
        if isinstance(error, exceptions.UserBlacklisted):
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
    bot.add_cog(Startup(bot))
    print(f"> Extension {__name__} is ready\n")
