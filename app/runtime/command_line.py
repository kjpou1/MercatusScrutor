import argparse
import os
from app.models.command_line_args import CommandLineArgs
#from app.config.config import Config


class CommandLine:
    @staticmethod
    def parse_arguments() -> CommandLineArgs:
        """
        Parse command line arguments and return an instance of CommandLineArgs.

        Returns:
            CommandLineArgs: The parsed command line arguments wrapped in a CommandLineArgs object.
        """
        # Load environment variables from Config
        #config = Config()

        # Create an ArgumentParser object to handle command line arguments
        parser = argparse.ArgumentParser(
            description='Run the application with specified arguments.'
        )

        # Add argument for scraping interval (in minutes)
        # This argument specifies how often the scraper should run
        parser.add_argument(
            '--scraping-interval', type=int,
            default=int(os.getenv('SCRAPING_INTERVAL', 30)),
            help='Time interval (in minutes) between each scraping process.'
        )

        # Add argument for the target URL to scrape from
        # This allows the user to specify which URL to target
        parser.add_argument(
            '--target-url', type=str,
            default=os.getenv('TARGET_URL', 'https://auchandrive.lu/historique-commandes'),
            help='URL to start scraping from.'
        )

        # Add argument for running the browser in headless mode
        # If specified, the scraper will run without opening a visible browser window
        parser.add_argument(
            '--headless', action='store_true',
            default=os.getenv('HEADLESS', 'false').lower() == 'true',
            help='Run the browser in headless mode.'
        )

        # Add arguments for username and password for signing in
        parser.add_argument(
            '--username', type=str,
            default=os.getenv('USERNAME'),
            help='Username for logging into the Auchan Drive account.'
        )
        parser.add_argument(
            '--password', type=str,
            default=os.getenv('PASSWORD'),
            help='Password for logging into the Auchan Drive account.'
        )

        # Parse the command line arguments
        args = parser.parse_args()

        # Create an instance of CommandLineArgs with parsed values
        return CommandLineArgs(
            scraping_interval=args.scraping_interval,  # Time interval between each scraping process
            target_url=args.target_url,  # The URL to scrape from
            headless=args.headless,  # Whether to run the browser in headless mode
            username=args.username,  # Username for authentication
            password=args.password  # Password for authentication
        )

if __name__ == "__main__":
    # Example usage: create an instance of CommandLine and parse arguments
    command_line = CommandLine()
    arguments = command_line.parse_arguments()
    # Print the parsed arguments (for debugging purposes)
    # This should be replaced with actual logic that uses these arguments
    print(arguments)