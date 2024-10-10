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

        if not self._is_initialized:
            self.logger = logging.getLogger(__name__)

            # General settings
            self._scraping_interval = int(self.get('SCRAPING_INTERVAL', 30))
            self._target_url = self.get('TARGET_URL', 'https://auchandrive.lu/historique-commandes')
            self._headless = self.get('HEADLESS', 'false').lower() == 'true'
            self._username = self.get('USERNAME')
            self._password = self.get('PASSWORD')
            self._history_file = self.get('ORDER_HISTORY_FILE', 'order_history.json')

            # Grocy API settings
            self._grocy_api_base = self.get('GROCY_API_BASE', 'http://hicsvntpi:9192')
            self._grocy_api_key = self.get('GROCY_API_KEY')

            # Thresholds and configurations
            self._similarity_threshold = float(self.get('SIMILARITY_THRESHOLD', 90))
            self._warning_similarity_threshold = float(self.get('WARNING_SIMILARITY_THRESHOLD', 75))
            self._live_stock_update = self.get('LIVE_STOCK_UPDATE', 'false').lower() == 'true'

            # Caching Time-to-Live (TTL) settings
            self._products_cache_ttl = int(self.get('PRODUCTS_CACHE_TTL', 600))  # Default 600 seconds (10 minutes)
            self._locations_cache_ttl = int(self.get('LOCATIONS_CACHE_TTL', 600))  # Default 600 seconds (10 minutes)

            self._is_initialized = True

    @classmethod
    def initialize(cls):
        """ Class method to explicitly initialize the Config singleton instance. """
        cls()

    @staticmethod
    def get(key, default=None):
        """ Static method to retrieve the value of an environment variable. """
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
        return self._live_stock_update

    @live_stock_update.setter
    def live_stock_update(self, value: bool):
        self._live_stock_update = value

    # Property for products_cache_ttl
    @property
    def products_cache_ttl(self) -> int:
        return self._products_cache_ttl

    @products_cache_ttl.setter
    def products_cache_ttl(self, value: int):
        self._products_cache_ttl = value

    # Property for locations_cache_ttl
    @property
    def locations_cache_ttl(self) -> int:
        return self._locations_cache_ttl

    @locations_cache_ttl.setter
    def locations_cache_ttl(self, value: int):
        self._locations_cache_ttl = value
