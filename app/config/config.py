import logging
import os
from dotenv import load_dotenv
from app.models import SingletonMeta

class Config(metaclass=SingletonMeta):
    """
    Configuration class that loads and stores application settings from environment variables.
    Utilizes the Singleton pattern to ensure only one instance exists throughout the application.
    """

    _is_initialized = False  # Class variable to prevent re-initialization

    def __init__(self):
        """
        Initialize the configuration by loading environment variables from a .env file
        and setting up application settings. This method ensures that initialization
        happens only once due to the Singleton pattern.
        """
        load_dotenv()  # Load environment variables from .env file into os.environ

        # Check if already initialized to prevent re-initialization
        if not self._is_initialized:
            # Set up a logger for the Config class
            self.logger = logging.getLogger(__name__)

            # Load general settings for the scraping process
            self._scraping_interval = int(self.get('SCRAPING_INTERVAL', 30))
            # Time interval in minutes between each scraping run

            self._target_url = self.get(
                'TARGET_URL',
                'https://auchandrive.lu/historique-commandes'
            )
            # The URL to start scraping from

            self._headless = self.get('HEADLESS', 'false').lower() == 'true'
            # Determines whether the browser runs in headless mode (True/False)

            self._username = self.get('USERNAME')
            # Username for logging into Auchan Drive

            self._password = self.get('PASSWORD')
            # Password for logging into Auchan Drive

            self._history_file = self.get('ORDER_HISTORY_FILE', 'order_history.json')
            # Path to the file where order history is stored

            # Load Grocy API-related settings
            self._grocy_api_base = self.get('GROCY_API_BASE', 'http://hicsvntpi:9192')
            # Base URL for the Grocy API

            self._grocy_api_key = self.get('GROCY_API_KEY')
            # API key for authenticating with the Grocy API
            
            self._similarity_threshold = float(self.get('SIMILARITY_THRESHOLD', 90))  
            # Default to 90% for product similarity threshold

            self._warning_similarity_threshold = float(self.get('WARNING_SIMILARITY_THRESHOLD', 75))
            # Default warning threshold at 75%

            self._live_stock_update = self.get('LIVE_STOCK_UPDATE', 'false').lower() == 'true'
            # Control whether live stock updates should occur (True/False)

            self._is_initialized = True  # Mark initialization as complete

    @classmethod
    def initialize(cls):
        """
        Class method to explicitly initialize the Config singleton instance.
        Ensures that the configuration is set up before use.
        """
        cls()

    @staticmethod
    def get(key, default=None):
        """
        Static method to retrieve the value of an environment variable.

        Parameters:
            key (str): The name of the environment variable to retrieve.
            default: The default value to return if the variable is not found.

        Returns:
            The value of the environment variable if it exists, otherwise the default value.
        """
        return os.getenv(key, default)

    # Property for scraping_interval
    @property
    def scraping_interval(self) -> int:
        return self._scraping_interval

    @scraping_interval.setter
    def scraping_interval(self, value: int):
        self._scraping_interval = value

    # Property for target_url
    @property
    def target_url(self) -> str:
        return self._target_url

    @target_url.setter
    def target_url(self, value: str):
        self._target_url = value

    # Property for headless
    @property
    def headless(self) -> bool:
        return self._headless

    @headless.setter
    def headless(self, value: bool):
        self._headless = value

    # Property for username
    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str):
        self._username = value

    # Property for password
    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    # Property for history_file
    @property
    def history_file(self) -> str:
        return self._history_file

    @history_file.setter
    def history_file(self, value: str):
        self._history_file = value

    # Property for grocy_api_base
    @property
    def grocy_api_base(self) -> str:
        return self._grocy_api_base

    @grocy_api_base.setter
    def grocy_api_base(self, value: str):
        self._grocy_api_base = value

    # Property for grocy_api_key
    @property
    def grocy_api_key(self) -> str:
        return self._grocy_api_key

    @grocy_api_key.setter
    def grocy_api_key(self, value: str):
        self._grocy_api_key = value

    # Property for similarity_threshold
    @property
    def similarity_threshold(self) -> float:
        return self._similarity_threshold

    @similarity_threshold.setter
    def similarity_threshold(self, value: float):
        self._similarity_threshold = value

    # Property for warning_similarity_threshold
    @property
    def warning_similarity_threshold(self) -> float:
        return self._warning_similarity_threshold

    @warning_similarity_threshold.setter
    def warning_similarity_threshold(self, value: float):
        self._warning_similarity_threshold = value

    # Property for live_stock_update
    @property
    def live_stock_update(self) -> bool:
        """
        Get the value of live stock update configuration.

        Returns:
            bool: True if live stock updates are enabled, False otherwise.
        """
        return self._live_stock_update

    @live_stock_update.setter
    def live_stock_update(self, value: bool):
        """
        Set the live stock update configuration.

        Parameters:
            value (bool): True to enable live stock updates, False to disable.
        """
        self._live_stock_update = value
