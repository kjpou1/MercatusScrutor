class Utils:
    @staticmethod
    def clean_string(value: str) -> str:
        """
        Static method to remove line feeds and trim leading/trailing whitespace from a string.
        
        :param value: The input string to clean.
        :return: The cleaned string.
        """
        return " ".join(value.split()).strip()