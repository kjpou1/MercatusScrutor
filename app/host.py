import asyncio
import logging
from app.config.config import Config
from app.models import CommandLineArgs
from app.services.auchan_order_service import AuchanOrderService
from app.runtime.command_line import CommandLine

class Host:
    def __init__(self, args: CommandLineArgs):
        """
        Initialize the Host class with command line arguments and configuration.

        Parameters:
        args (CommandLineArgs): Command line arguments passed to the script.
        """
        self.config = Config()
        self.args = args
        self.logger = logging.getLogger(__name__)
        
        # Override Config with values from CommandLineArgs
        if args.scraping_interval:
            self.config.scraping_interval = args.scraping_interval
        if args.target_url:
            self.config.target_url = args.target_url
        if args.headless is not None:
            self.config.headless = args.headless
        if args.username:
            self.config.username = args.username
        if args.password:
            self.config.password = args.password

        self.auchan_order_service = AuchanOrderService()
        self.scraping_interval = self.config.scraping_interval 
        
    def run(self):
        """
        Run the asynchronous run_async method.
        """
        return asyncio.run(self.run_async())

    async def run_async(self):
        """
        Asynchronous method to perform the main logic.
        """
        self.logger.info("Starting host process with a scraping interval of %d minutes.", self.scraping_interval)

        while True:
            try:
                self.logger.info("Starting scraping process.")
                await self.auchan_order_service.scrape_auchan_order_history()
            except Exception as e:
                self.logger.error(f"An error occurred during scraping: {e}")

            # Wait for the specified scraping interval (convert to seconds)
            self.logger.info(f"Waiting for {self.scraping_interval} minutes until next scraping run.")
            await asyncio.sleep(self.scraping_interval * 60)
            
if __name__ == '__main__':
    # Setup logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Parse command line arguments
    args = CommandLine.parse_arguments()
    host = Host(args)
    host.run()