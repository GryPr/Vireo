import os

import exceptions


def check_mandatory_env_vars() -> None:
    """
    Check that all the mandatory environment variables are defined.
    """
    mandatory_env_vars = {"BOT_TOKEN", "MARIADB_USER", "MARIADB_PASSWORD"}
    missing_env_vars = mandatory_env_vars - set(os.environ)
    if missing_env_vars:
        raise exceptions.EnvironmentVariablesMissingError(missing_env_vars)
