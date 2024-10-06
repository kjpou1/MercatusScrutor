import logging
import asyncio
import json
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from app.config.config import Config


class AuchanOrderService:
    def __init__(self):
        """
        Initialize the AuchanOrderService class with configuration and logger.
        """
        self.config = Config()  # Use the global configuration instance
        self.logger = logging.getLogger(__name__)

    async def scrape_auchan_order_history(self):
        """
        Asynchronous method to scrape the Auchan Drive order history.
        """
        self.logger.info("Starting Auchan order history scraping process.")

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
            await page.goto(target_url)
            await page.wait_for_selector("table.table")

            orders = []
            rows = await page.query_selector_all("table.table tbody tr")
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

                    # Append order details to the list
                    orders.append({
                        "order_number": order_number,
                        "reference": reference,
                        "date": date,
                        "total_price": total_price,
                        "pickup_point": pickup_point,
                        "payment_method": payment_method,
                        "status": status,
                        "details_link": details_link
                    })

                except Exception as e:
                    self.logger.error(f"Failed to extract order details for row: {e}")
                    continue  # Skip to the next row in case of an error

            # Iterate through the orders to extract detailed information
            for order in orders:
                details_link = order.get("details_link")
                if details_link:
                    try:
                        await page.goto(details_link)
                        await page.wait_for_load_state('domcontentloaded')  # Ensure page is fully loaded
                        order_details = await self.extract_order_details(page)
                        order["details"] = order_details
                        self.logger.debug(f"Order Details for {order['order_number']}: {order_details}")
                    except Exception as e:
                        self.logger.error(f"Failed to extract detailed order information for {order['order_number']}: {e}")
                        continue

            # Save the orders to a JSON file
            try:
                with open('order_history.json', 'w', encoding='utf-8') as f:
                    json.dump(orders, f, ensure_ascii=False, indent=4)
                self.logger.info("Order history successfully saved to order_history.json.")
            except Exception as e:
                self.logger.error(f"Failed to save order history to JSON file: {e}")

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
                category_element = await product.query_selector(".category span")
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

                # Combine product name and description
                product_full_name = f"{product_name} {product_description}".strip()

                if product_full_name:
                    details[product_full_name] = {
                        "category": current_category,
                        "quantity": quantity.strip(),
                        "unit_price": unit_price.strip(),
                        "total_price": total_price.strip(),
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