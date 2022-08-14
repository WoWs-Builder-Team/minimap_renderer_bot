import os

from utils.exceptions import MissingEnvironmentVariableError


def check_environment_var(variables: list[str]):
    for variable in variables:
        if not os.getenv(variable):
            raise MissingEnvironmentVariableError(
                f"Missing environment variable: {variable}"
            )
