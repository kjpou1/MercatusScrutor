import logging
from app.helpers.utils import Utils
from app.services.grocy_service import GrocyService
from app.helpers.matching_utils import MatchingUtils  
from app.config.config import Config

class InventoryService:
    def __init__(self):
        """
        Initialize the InventoryService by setting up the GrocyService and logger.
        """
        self.grocy_service = GrocyService()  
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        self.similarity_threshold = self.config.similarity_threshold  # Use the threshold from the config

    def process_order(self, order):
        """
        Main function to process an order by matching products and updating stock if necessary.

        Parameters:
            order (dict): The order structure that contains order details.

        Returns:
            dict: A dictionary with product matches, their quantities, and location, or None if no match found.
        """
        self.logger.info("Processing order with order number: %s", order.get("order_number"))
        
        products = self.fetch_products()
        if not products:
            return None
        
        parking_location_id = self.find_parking_location()
        if not parking_location_id:
            return None

        order_details = order.get("details", {})
        matched_products = {}

        for product_name, product_info in order_details.items():
            self.logger.info(f"Looking for product: {product_name} in Grocy inventory")
            
            best_match, similarity_percentage = self.match_product(product_name, products)
            if not best_match:
                continue

            if similarity_percentage >= self.similarity_threshold:
                self.logger.info(f"Product {best_match['name']} found with similarity {similarity_percentage:.2f}%")
                unit_price = self.convert_unit_price(product_info.get('unit_price', '0.0'))
                order_quantity = product_info.get('quantity', 1)

                if self.config.live_stock_update:
                    self.update_stock(best_match['id'], order_quantity, parking_location_id, unit_price)

                matched_products[product_name] = self.build_matched_product_info(
                    best_match, order_quantity, unit_price, similarity_percentage, parking_location_id
                )
            else:
                self.log_warning_for_low_similarity(product_name, best_match, similarity_percentage)

        return matched_products if matched_products else None

    def fetch_products(self):
        """Fetch product list from Grocy."""
        products = self.grocy_service.fetch_products()
        if not products:
            self.logger.error("Failed to fetch products from Grocy API")
        return products

    def find_parking_location(self):
        """Find and return the ID of the 'Parking' location."""
        locations = self.grocy_service.fetch_locations()
        if not locations:
            self.logger.error("Failed to fetch locations from Grocy API")
            return None

        parking_location_match = MatchingUtils.get_best_match("Parking", locations)
        if not parking_location_match:
            self.logger.warning("No matching location found for 'Parking'")
            return None
        
        parking_location_id = parking_location_match['product']['id']
        self.logger.info(f"Location 'Parking' found with location ID: {parking_location_id}")
        return parking_location_id

    def match_product(self, product_name, products):
        """
        Match a product name from the order to a product in Grocy.

        Returns:
            tuple: Matched product and similarity percentage, or None if not found.
        """
        best_match = MatchingUtils.get_best_match(product_name, products)
        if best_match:
            return best_match['product'], best_match['similarity_percentage']
        else:
            self.logger.warning(f"Product {product_name} not found in Grocy.")
            return None, 0

    def convert_unit_price(self, unit_price_str):
        """
        Convert unit price string to a float. Logs an error if conversion fails.

        Returns:
            float: Converted unit price or 0.0 if invalid.
        """
        try:
            return float(Utils.clean_price(unit_price_str))
        except ValueError as e:
            self.logger.error(f"Failed to convert unit price {unit_price_str}: {e}")
            return 0.0

    def update_stock(self, product_id, order_quantity, location_id, unit_price):
        """
        Update stock in Grocy by adding the product to the inventory.
        
        Parameters:
            product_id (int): The ID of the product to update.
            order_quantity (float): The quantity to add to the stock.
            location_id (int): The location ID where the product is stored.
            unit_price (float): The unit price of the product.
        """
        response = self.grocy_service.add_to_stock(product_id, order_quantity, location_id, unit_price)
        if response is None:
            self.logger.error(f"Failed to add product {product_id} to stock.")

    def build_matched_product_info(self, grocy_product, order_quantity, unit_price, similarity_percentage, location_id):
        """
        Build the matched product info dictionary for logging and return.

        Returns:
            dict: A dictionary of matched product details.
        """
        return {
            "grocy_product_name": grocy_product['name'],
            "grocy_product_id": grocy_product['id'],
            "quantity_in_grocy": grocy_product.get('stock_amount', 'N/A'),
            "order_quantity": order_quantity,
            "unit_price": unit_price,
            "similarity_percentage": similarity_percentage,
            "location": {
                "location_id": location_id,
                "similarity_percentage": similarity_percentage,
            }
        }

    def log_warning_for_low_similarity(self, product_name, grocy_product, similarity_percentage):
        """Log a warning for low similarity between the order product and the Grocy product."""
        if similarity_percentage >= self.config.warning_similarity_threshold:
            self.logger.warning(f"Order Product {product_name} skipped due to low similarity ({similarity_percentage:.2f}%) "
                                f"with Grocy Product {grocy_product['name']}.")
