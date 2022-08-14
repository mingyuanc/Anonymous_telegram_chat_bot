import logging
import os
from typing import Optional, Dict


class APIConfig:
    REQUIRED_VARS = ["SQL_HOST",
                     'SQL_DATABASE',
                     'SQL_USER',
                     "SQL_PASSWORD",
                     "SQL_PORT",
                     "ADMIN_ID",
                     "TELEGRAM_API"]

    def __init__(self, logger: Optional[logging.Logger] = None):
        self._logger = logger if logger is not None else logging.getLogger(
            self.__class__.__name__)  # type: ignore
        self.config = self._validate_and_load_config()
        # self._logger.info(f'Starting with config: {self.config}')
        # Only used for debugging

    def _validate_and_load_config(self) -> Dict:
        """ Validates and loads all config parameters from files or env vars

        In this method, you can implement loading and validation logic for your
        deployment. The idea to run the validation here is to make sure that a
        faulty configuration is identified when starting the app instead of
        during the runtime through and application crash.

        Returns:
            Dict -- Config
        """
        config = {}

        for f in self.REQUIRED_VARS:
            if f not in os.environ:
                raise ValueError(f'Environment variable {f} is required.')
            else:
                config[f] = os.environ[f]
        return config
