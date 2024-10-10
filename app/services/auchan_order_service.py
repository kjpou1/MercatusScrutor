import logging
import asyncio
import json
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from app.config.config import Config
from app.helpers.utils import Utils
import os
from app.services.inventory_service import InventoryService

class AuchanOrderService:
    def __init__(self):
        """
        Initialize the AuchanOrderService class with configuration and logger.
        """
        self.config = Config()  # Use the global configuration instance
        self.logger = logging.getLogger(__name__)
        self.history_file = self.config.history_file
        self.order_history = []  # Store existing orders with details
        self.existing_order_ids = {}  # Map of order_number -> order details
        self.inventory_service = InventoryService()  # Instantiate InventoryService for inventory management

    def load_order_history(self):
        """Loads the existing order history from the JSON file."""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as file:
                self.order_history = json.load(file)
                self.existing_order_ids = {order['order_number']: order for order in self.order_history}
        else:
            self.order_history = []
            self.existing_order_ids = {}

    def save_order_history(self, new_orders):
        """Saves the updated order history to the JSON file with updated orders in place and new orders pre-appended."""
        
        # Load the existing orders if the file exists
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as file:
                existing_orders = json.load(file)
        else:
            existing_orders = []

        # Dictionary for quick lookup of existing orders by order_number
        existing_orders_map = {order['order_number']: order for order in existing_orders}

        # Prepare a list for updated orders, maintaining the original order in the history
        updated_existing_orders = []
        
        # Process new orders
        for new_order in new_orders:
            order_number = new_order['order_number']
            
            # If order exists, update it in place
            if order_number in existing_orders_map:
                existing_orders_map[order_number].update(new_order)
            else:
                # If it's a new order, add to the updated_existing_orders list (pre-append new orders)
                updated_existing_orders.append(new_order)

        # Combine updated existing orders with the new ones at the beginning
        combined_orders = updated_existing_orders + list(existing_orders_map.values())
        
        # Save the updated order history back to the file
        with open(self.history_file, 'w', encoding='utf-8') as file:
            json.dump(combined_orders, file, ensure_ascii=False, indent=4)

        self.logger.info("Order history successfully updated with in-place modifications.")

    
    def process_orders(self, new_orders):
        """Processes new orders, updating the status if necessary."""
        updated_orders = []
        new_order_list = []

        for new_order in new_orders:
            order_number = new_order['order_number']
            new_order['status'] = new_order['status'].lower()  # Ensure status is always lowercase

            if order_number in self.existing_order_ids:
                existing_order = self.existing_order_ids[order_number]
                existing_order['status'] = existing_order['status'].lower()  # Ensure existing status is lowercase

                # Check if status has changed
                if new_order['status'] != existing_order['status']:
                    self.logger.info(f"Order {order_number} has a status update: {existing_order['status']} -> {new_order['status']}")

                    # Store the previous status
                    new_order['previous_status'] = existing_order['status']

                    # Add current processing status field
                    new_order['processing_status'] = "pending"

                    # If the status is "annulé", update the order but do not read details again
                    if new_order['status'] == "annulé":
                        existing_order.update(new_order)
                        updated_orders.append(existing_order)
                        self.logger.info(f"Skipping detail processing for order {order_number} (status: annulé).")
                    else:
                        # Update the order and mark for detail processing
                        existing_order.update(new_order)
                        updated_orders.append(existing_order)
                        self.logger.info(f"Processing details for updated order {order_number}.")
                        yield existing_order  # Send the order for detail processing
            else:
                # New order, process it and add to the list
                self.logger.info(f"New order found: {order_number}. Processing details.")
                new_order['previous_status'] = None  # New order, no previous status

                # Set processing status based on current order status
                if new_order['status'] == "livré":
                    new_order['processing_status'] = "processed"
                else:
                    new_order['processing_status'] = "pending"

                new_order_list.append(new_order)
                yield new_order  # Send the order for detail processing

        # Save updated and new orders
        if updated_orders or new_order_list:
            self.save_order_history(new_order_list + updated_orders)
        else:
            self.logger.info("No new or updated orders to process.")



    async def scrape_auchan_order_history(self):
        """
        Asynchronous method to scrape the Auchan Drive order history.
        """
        self.logger.info("Starting Auchan order history scraping process.")

        # Load the existing order history
        self.load_order_history()

        # Load configuration settings
        target_url = self.config.target_url
        headless = self.config.headless  # Read headless mode from configuration
        username = self.config.username
        password = self.config.password

        # Validate that username and password are available
        if not username or not password:
            self.logger.error("Username or password not provided. Cannot proceed with scraping.")
            return

        # Launch Playwright browser
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()
            page = await context.new_page()

            # Navigate to Auchan Drive login page
            await page.goto(target_url)

            # Log in using credentials
            await page.fill("input[name='email']", username)
            await page.fill("input[name='password']", password)
            await page.click("button:has-text('SE CONNECTER')")

            # Wait for successful navigation after login
            try:
                await page.wait_for_selector("text=Mon compte", timeout=10000)
                self.logger.info("Successfully logged in.")
            except PlaywrightTimeoutError as e:
                self.logger.error(f"Login failed: {e}")
                await browser.close()
                return

            # Extract order information from table rows into a data structure
            self.logger.info("Extracting order history.")
            await page.goto(target_url)
            await page.wait_for_selector("table.table")

            orders = []
            rows = await page.query_selector_all("table.table tbody tr")
            self.logger.info("Processing %s rows.", len(rows))
            for row in rows:
                try:
                    order_number_element = await row.query_selector("td:nth-child(1)")
                    reference_element = await row.query_selector("th[scope='row']")
                    date_element = await row.query_selector("td:nth-child(3)")
                    total_price_element = await row.query_selector("td:nth-child(4)")
                    pickup_point_element = await row.query_selector("td:nth-child(5)")
                    payment_method_element = await row.query_selector("td:nth-child(6)")
                    status_element = await row.query_selector("td:nth-child(7) span")
                    details_link_element = await row.query_selector("a[data-link-action='view-order-details']")

                    # Extract text content or attributes from elements
                    order_number = await order_number_element.text_content() if order_number_element else None
                    reference = await reference_element.text_content() if reference_element else None
                    date = await date_element.text_content() if date_element else None
                    total_price = await total_price_element.text_content() if total_price_element else None
                    pickup_point = await pickup_point_element.text_content() if pickup_point_element else None
                    payment_method = await payment_method_element.text_content() if payment_method_element else None
                    status = await status_element.text_content() if status_element else None
                    details_link = await details_link_element.get_attribute("href") if details_link_element else None

                    # Process only new orders or orders with updated status
                    if order_number and order_number.isnumeric() and status:
                        orders.append({
                            "order_number": order_number,
                            "reference": reference,
                            "date": Utils.clean_dates(date),
                            "total_price": Utils.clean_price(total_price),
                            "pickup_point": pickup_point,
                            "payment_method": payment_method,
                            "status": Utils.clean_string(status),
                            "details_link": details_link
                        })

                except Exception as e:
                    self.logger.error(f"Failed to extract order details for row: {e}")
                    continue  # Skip to the next row in case of an error

            # Process new and updated orders (yielding orders needing detail processing)
            for order in self.process_orders(orders):
                details_link = order.get("details_link")
                if details_link:
                    try:
                        await page.goto(details_link)
                        await page.wait_for_load_state('domcontentloaded')  # Ensure page is fully loaded
                        order_details = await self.extract_order_details(page)
                        order["details"] = order_details
                        self.logger.debug(f"Order Details for {order['order_number']}: {order_details}")

                        # Now that the details are fetched, process the order with the InventoryService
                        if order['status'] == 'livré':
                            self.inventory_service.process_order(order)  # Call the InventoryService
                            self.logger.info(f"Inventory updated for order {order['order_number']}.")

                    except Exception as e:
                        self.logger.error(f"Failed to extract detailed order information for {order['order_number']}: {e}")
                        continue

            # Close the browser
            await browser.close()


    async def extract_order_details(self, page):
        """
        Extract details of the order from the page.
        
        Parameters:
            page: Playwright page object.
        
        Returns:
            dict: A dictionary containing details of the order.
        """
        try:
            details = {}
            products = await page.query_selector_all("#order-products tbody tr")
            current_category = None

            for product in products:
                # Check if the row is a category row
                category_element = await product.query_selector("td > span")
                if category_element:
                    current_category = (await category_element.text_content()).strip()
                    continue
                
                # Attempt to locate the elements for product name, description, quantity, unit price, and total price.
                product_name_element = await product.query_selector(".manufacturer-name")
                product_description_element = await product.query_selector("strong > a")
                quantity_element = await product.query_selector("td:nth-child(2)")
                unit_price_element = await product.query_selector("td:nth-child(3)")
                total_price_element = await product.query_selector("td:nth-child(4)")
                discount_element = await product.query_selector(".ri-block.product-line-discount span")
                cagnotte_element = await product.query_selector(".cagnotte-block.product-line-discount span")

                # Extract the text content from each element.
                product_name = await product_name_element.text_content() if product_name_element else ""
                product_description = await product_description_element.text_content() if product_description_element else ""
                quantity = await quantity_element.text_content() if quantity_element else ""
                unit_price = await unit_price_element.text_content() if unit_price_element else ""
                total_price = await total_price_element.text_content() if total_price_element else ""
                discount = await discount_element.text_content() if discount_element else ""
                cagnotte = await cagnotte_element.text_content() if cagnotte_element else ""

                # Do some cleanup of the data
                product_name = Utils.clean_string(product_name)
                product_description = Utils.clean_string(product_description)
                discount = Utils.extract_numeric_value(discount)
                cagnotte = Utils.extract_numeric_value(cagnotte)
                
                # Ensure the description doesn't duplicate the name
                if product_description.startswith(product_name):
                    product_full_name = product_description  # Use only the description if it already includes the name
                else:
                    product_full_name = f"{product_name} {product_description}".strip()  # Concatenate if they're different
   
                if product_full_name:
                    details[product_full_name] = {
                        "name": product_name,
                        "description": product_description,
                        "category": current_category,
                        "quantity": quantity.strip(),
                        "unit_price": Utils.clean_price(unit_price.strip()),
                        "total_price": Utils.clean_price(total_price.strip()),
                        "discount": discount.strip(),
                        "cagnotte": cagnotte.strip()
                    }
                    
            return details
        except Exception as e:
            self.logger.error(f"Failed to extract order details: {e}")
            return {}

if __name__ == "__main__":
    # Example usage
    order_service = AuchanOrderService()
    asyncio.run(order_service.scrape_auchan_order_history())
