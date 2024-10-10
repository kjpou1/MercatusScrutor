from datetime import datetime
import re

class Utils:
    @staticmethod
    def clean_string(value: str) -> str:
        """
        Static method to remove line feeds and trim leading/trailing whitespace from a string.
        
        :param value: The input string to clean.
        :return: The cleaned string.
        """
        if value:
            return " ".join(value.split()).strip()
        else:
            return value
        
    @staticmethod
    def extract_numeric_value(value: str) -> str:
        """
        Static method to remove non-numeric characters, leaving only numeric amounts. 
        Handles both commas and periods as decimal separators.
        
        :param value: The input string to clean.
        :return: The cleaned string containing only the numeric value.
        """
        # Replace commas with periods (for locales using commas as decimal separators)
        value = value.replace(",", ".")
        # Use regex to remove everything except digits and periods
        return re.sub(r'[^\d.]', '', value).strip()
    
    @staticmethod
    def clean_price(value: str) -> str:
        """
        Static method to clean individual price fields by splitting on newlines and applying extract_numeric_value.
        
        :param value: The input string (price) to clean.
        :return: The cleaned price string.
        """
        # Take only the first part after splitting by newline characters
        price_cleaned = Utils.clean_string(value) #value.split("\n")[0].strip()
        # Apply extract_numeric_value to remove any remaining unnecessary characters
        return Utils.extract_numeric_value(price_cleaned)

    @staticmethod
    def clean_prices(item_data: dict) -> dict:
        """
        Cleans both total_price and unit_price fields by using clean_price method.
        
        :param item_data: The dictionary containing the item's total_price and unit_price.
        :return: The cleaned dictionary with properly structured total_price and unit_price.
        """
        # Clean total_price
        item_data["total_price"] = Utils.clean_price(item_data.get("total_price", ""))

        # Clean unit_price
        item_data["unit_price"] = Utils.clean_price(item_data.get("unit_price", ""))

        return item_data
    
    @staticmethod
    def clean_dates(date_str: str) -> str:
        """
        Static method to check if a date is in ISO format (YYYY-MM-DD).
        If not, it converts the date to this format.
        
        :param date_str: The input date string.
        :return: The date in ISO format (YYYY-MM-DD).
        """
        try:
            # Try to parse the date assuming it's already in ISO format
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # If the date is in a different format, try various other formats
            possible_formats = [
                "%d/%m/%Y",  # DD/MM/YYYY
                "%m/%d/%Y",  # MM/DD/YYYY
                "%B %d, %Y", # Full month name, day, year
                "%d-%b-%Y",  # DD-Mon-YYYY
                "%Y/%m/%d"   # YYYY/MM/DD
            ]
            for fmt in possible_formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                # If none of the formats match, return the original string (or you can flag it)
                return "[Invalid Date]"

        # Return the date in ISO format
        return date_obj.strftime("%Y-%m-%d")
