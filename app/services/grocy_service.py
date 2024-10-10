import requests
import logging
from app.config.config import Config
from cachetools import TTLCache

class GrocyService:
    def __init__(self):
        """
        Initialize the GrocyService class by loading the necessary configuration
        settings for interacting with the Grocy API, including the base API URL
        and the API key. Also, set up TTL caching for products and locations.
        """
        self.config = Config()  # Load configuration settings from the global config
        self.api_base = self.config.grocy_api_base  # Base URL for the Grocy API
        self.api_key = self.config.grocy_api_key  # API key for authentication
        self.logger = logging.getLogger(__name__)  # Initialize logger for the service

        # Headers required for making authenticated API requests
        self.headers = {
            "GROCY-API-KEY": self.api_key
        }

        # Set up TTL cache for products and locations (TTL values from config)
        self.products_cache = TTLCache(maxsize=100, ttl=self.config.products_cache_ttl)  # Cache for products
        self.locations_cache = TTLCache(maxsize=50, ttl=self.config.locations_cache_ttl)  # Cache for locations

    def fetch_products(self):
        """
        Fetch a list of products from the Grocy API using a GET request.
        Cached for the duration specified by the PRODUCTS_CACHE_TTL setting.
        
        Returns:
            dict: The JSON response from the API if successful, or None if failed.
        """
        if 'products' in self.products_cache:
            self.logger.info("Fetching products from cache.")
            return self.products_cache['products']

        url = f"{self.api_base}/api/objects/products"
        try:
            self.logger.info(f"Fetching products from Grocy API: {url}")
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                self.logger.info("Successfully fetched products from Grocy API.")
                products = response.json()
                self.products_cache['products'] = products  # Cache the result
                return products
            else:
                self.logger.error(f"Failed to fetch products: {response.status_code}")
                return None

        except requests.RequestException as e:
            self.logger.error(f"An error occurred while fetching products: {e}")
            return None

    def fetch_locations(self):
        """
        Fetch a list of locations from the Grocy API using a GET request.
        Cached for the duration specified by the LOCATIONS_CACHE_TTL setting.
        
        Returns:
            dict: The JSON response from the API if successful, or None if failed.
        """
        if 'locations' in self.locations_cache:
            self.logger.info("Fetching locations from cache.")
            return self.locations_cache['locations']

        url = f"{self.api_base}/api/objects/locations"
        try:
            self.logger.info(f"Fetching locations from Grocy API: {url}")
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                self.logger.info("Successfully fetched locations from Grocy API.")
                locations = response.json()
                self.locations_cache['locations'] = locations  # Cache the result
                return locations
            else:
                self.logger.error(f"Failed to fetch locations: {response.status_code}")
                return None

        except requests.RequestException as e:
            self.logger.error(f"An error occurred while fetching locations: {e}")
            return None

    def add_to_stock(self, product_id, amount, location_id, total_price):
        """
        Add a product to Grocy stock by sending a POST request to the Grocy stock API,
        including the total price of the product.

        Parameters:
            product_id (int): The ID of the product to add to the stock.
            amount (float): The quantity to add to the stock.
            location_id (int): The location ID where the product is being stored.
            total_price (float): The total price of the product to store in the inventory.

        Returns:
            dict: The JSON response from the API if successful, or None if failed.
        """
        url = f"{self.api_base}/api/stock/products/{product_id}/add"
        payload = {
            "amount": amount,
            "location_id": location_id,
            "price": total_price  # Include the total price in the payload
        }

        try:
            self.logger.info(f"Adding product ID {product_id} to stock at location ID {location_id} with total price: {total_price}.")
            response = requests.post(url, headers=self.headers, json=payload)

            if response.status_code == 200:
                self.logger.info(f"Successfully added product ID {product_id} to stock with price {total_price}.")
                return response.json()
            else:
                self.logger.error(f"Failed to add product to stock: {response.status_code}, Response: {response.text}")
                return None

        except requests.RequestException as e:
            self.logger.error(f"An error occurred while adding product to stock: {e}")
            return None
