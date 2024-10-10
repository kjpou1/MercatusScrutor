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
        Process an order by reading its details and searching for matching products in the Grocy API.
        Products with a similarity percentage above the threshold are added to the Grocy stock using their unit price.

        Parameters:
            order (dict): The order structure that contains order details.

        Returns:
            dict: A dictionary with product matches, their quantities, and location, or None if no match found.
        """
        self.logger.info("Processing order with order number: %s", order.get("order_number"))

        # Fetch the product list from Grocy
        products = self.grocy_service.fetch_products()
        if not products:
            self.logger.error("Failed to fetch products from Grocy API")
            return None

        # Fetch the locations list from Grocy
        locations = self.grocy_service.fetch_locations()
        if not locations:
            self.logger.error("Failed to fetch locations from Grocy API")
            return None

        # Use MatchingUtils to find the best match for the "Parking" location
        parking_location_match = MatchingUtils.get_best_match("Parking", locations)
        if not parking_location_match:
            self.logger.warning("No matching location found for 'Parking'")
            return None

        parking_location = parking_location_match['product']
        parking_location_id = parking_location['id']
        self.logger.info(f"Location 'Parking' found with location ID: {parking_location_id}")

        # Order details structure (e.g., {'Pavés de Saumon x4 500g': {...}})
        order_details = order.get("details", {})
        matched_products = {}

        # Iterate through the order details to find corresponding products in the Grocy inventory
        for product_name, product_info in order_details.items():
            self.logger.info(f"Looking for product: {product_name} in Grocy inventory")

            # Use MatchingUtils to find the best match for the product in the Grocy product list
            best_match = MatchingUtils.get_best_match(product_name, products)

            if best_match:
                grocy_product = best_match['product']
                similarity_percentage = best_match['similarity_percentage']

                # Only add the product to stock if the similarity percentage is above the threshold
                if similarity_percentage >= self.similarity_threshold:
                    self.logger.info(f"Product found: {grocy_product['name']} in Grocy inventory with similarity: {similarity_percentage:.2f}%")
                    order_quantity = product_info.get('quantity', 1)  # Default to 1 if no quantity is provided
                    unit_price_str = product_info.get('unit_price', '0.0')  # Extract unit price as string

                    # Clean and convert unit price to float
                    try:
                        unit_price = float(Utils.clean_price(unit_price_str))  
                    except ValueError as e:
                        self.logger.error(f"Failed to convert unit price {unit_price_str} for product {product_name}: {e}")
                        unit_price = 0.0  # Default to 0.0 if conversion fails

                    # Skip stock update if unit price is invalid or missing
                    if not unit_price_str or unit_price == 0.0:
                        self.logger.warning(f"Missing or invalid unit price for {product_name}, skipping stock update.")
                        continue

                    # Check if live stock updates are enabled
                    if self.config.live_stock_update:
                        response = self.grocy_service.add_to_stock(grocy_product['id'], float(order_quantity), parking_location_id, unit_price)
                        if response is None:
                            self.logger.error(f"Failed to add product {grocy_product['name']} to stock.")

                    # Record the matched product details
                    matched_products[product_name] = {
                        "grocy_product_name": grocy_product['name'],
                        "grocy_product_id": grocy_product['id'],
                        "quantity_in_grocy": grocy_product.get('stock_amount', 'N/A'),
                        "order_quantity": order_quantity,
                        "unit_price": unit_price,
                        "similarity_percentage": similarity_percentage,
                        "location": {
                            "name": parking_location['name'],
                            "location_id": parking_location_id,
                            "similarity_percentage": parking_location_match['similarity_percentage']
                        }
                    }
                else:
                    if similarity_percentage >= self.config.warning_similarity_threshold:
                        self.logger.warning(f"Order Product {product_name} skipped due to low similarity ({similarity_percentage:.2f}%) with Product {grocy_product['name']}.")
            else:
                self.logger.warning(f"Product not found in Grocy: {product_name}")

        return matched_products if matched_products else None
