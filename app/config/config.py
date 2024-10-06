import logging
import os
from dotenv import load_dotenv
from app.models import SingletonMeta

class Config(metaclass=SingletonMeta):
    _is_initialized = False

    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        # Prevent re-initialization
        if not self._is_initialized:
            # Initialize configuration settings
            self.logger = logging.getLogger(__name__)
            # Load initial values from environment variables
            self._scraping_interval = int(self.get('SCRAPING_INTERVAL', 30))
            self._target_url = self.get('TARGET_URL', 'https://auchandrive.lu/historique-commandes')
            self._headless = self.get('HEADLESS', 'false').lower() == 'true'
            self._username = self.get('USERNAME')
            self._password = self.get('PASSWORD')
            self._history_file = self.get('ORDER_HISTORY_FILE', 'order_history.json')  # History file path
            self._is_initialized = True

    @classmethod
    def initialize(cls):
        # Convenience method to explicitly initialize the Config
        cls()

    @staticmethod
    def get(key, default=None):
        """
        Get the value of an environment variable.

        Parameters:
            key (str): The name of the environment variable.
            default: The default value if the environment variable is not found.

        Returns:
            The value of the environment variable or the default value.
        """
        return os.getenv(key, default)

    @property
    def scraping_interval(self) -> int:
        return self._scraping_interval

    @scraping_interval.setter
    def scraping_interval(self, value: int):
        self._scraping_interval = value

    @property
    def target_url(self) -> str:
        return self._target_url

    @target_url.setter
    def target_url(self, value: str):
        self._target_url = value

    @property
    def headless(self) -> bool:
        return self._headless

    @headless.setter
    def headless(self, value: bool):
        self._headless = value

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def history_file(self) -> str:
        return self._history_file

    @history_file.setter
    def history_file(self, value: str):
        self._history_file = value
