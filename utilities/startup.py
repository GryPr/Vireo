"""Startup related utility functions."""
import os

import disnake
from disnake.ext.commands import Bot
from exceptions import EnvironmentVariablesMissingError


def run_sanity_checks() -> None:
    """Ensure that the environment is properly set up."""
    check_mandatory_env_vars()


def create_bot() -> Bot:
    """Create and returned a modified Bot object."""
    bot = Bot(command_prefix=os.environ.get("PREFIX", default="v!"),
              intents=disnake.Intents.all(),
              help_command=None,
              sync_commands_debug=True,
              sync_permissions=True)

    # TODO: replace the help command rather than removing it
    bot.remove_command("help")

    return bot


def check_mandatory_env_vars() -> None:
    """Check that all the mandatory environment variables are defined."""
    mandatory_env_vars = {"BOT_TOKEN", "MARIADB_USER", "MARIADB_PASSWORD"}
    missing_env_vars = mandatory_env_vars - set(os.environ)
    if missing_env_vars:
        raise EnvironmentVariablesMissingError(missing_env_vars)


def load_extensions(bot: Bot, file_path: str) -> None:
    """Load bot extension files.

    :param bot: the bot which will load the extensions
    :param file_path: directory from which to load extensions, package sub-directories will also be loaded
    """
    bot.load_extensions(file_path)


def run_bot(bot: Bot) -> None:
    """Run the bot with the BOT_TOKEN."""
    bot.run(os.environ.get("BOT_TOKEN"))
