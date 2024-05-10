import logging
from os import environ as env
from os import path
from typing import Optional

logger = logging.getLogger(__name__)


class Credentials:
    """
    The main class used to read credentials.
    """

    directory: Optional[str]
    encoding: str
    env_prefix: str
    env_fallback: bool

    def __init__(
        self,
        encoding: str = "utf-8",
        env_fallback: bool = True,
        env_prefix: str = "",
    ) -> None:
        self.encoding = encoding
        self.env_fallback = env_fallback
        self.env_prefix = env_prefix

        self.directory = env.get("CREDENTIALS_DIRECTORY")

        if self.directory is None:
            logger.info("No credentials directory found.")

            if not self.env_fallback:
                raise RuntimeError(
                    "No credentials directory exists and env variables fallback is disabled, no secrets can be fetched."
                )

    def __getitem__(self, key: str) -> str:
        if self.directory is not None:
            try:
                with open(path.join(self.directory, key), encoding=self.encoding) as fp:
                    return fp.read().removesuffix("\n")

            except FileNotFoundError:
                logger.debug(f"{key} was not found in the credentials directory.")

                if not self.env_fallback:
                    # If no credential exists and no fallback is available, raise an error
                    raise KeyError(f"{key} doesn't exist in the credentials directory.")

        value = env.get(f"{self.env_prefix}{key}")

        if value is None:
            raise KeyError(
                f"{key} not found, in the credentials directory or the environment."
            )

        return value
