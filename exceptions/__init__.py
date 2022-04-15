class UserBlacklisted(Exception):
    """
    Thrown when a user is attempting something, but is blacklisted.
    """

    def __init__(self, message="User is blacklisted!"):
        self.message = message
        super().__init__(self.message)


class UserNotOwner(Exception):
    """
    Thrown when a user is attempting something, but is not an owner of the bot.
    """

    def __init__(self, message="User is not an owner of the bot!"):
        self.message = message
        super().__init__(self.message)


class EnvironmentVariablesMissingError(Exception):
    """
    Thrown when at least one environment variable is missing.
    """

    def __init__(
        self,
        missing_env_vars: set[str],
        message="These environment variables aren't defined",
    ):
        super().__init__(f"{message}: {missing_env_vars}")
