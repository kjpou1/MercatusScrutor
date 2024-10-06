import asyncio
import logging
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
        self.args = args
        self.logger = logging.getLogger(__name__)
        self.auchan_order_service = AuchanOrderService()

    def run(self):
        """
        Run the asynchronous run_async method.
        """
        return asyncio.run(self.run_async())

    async def run_async(self):
        """
        Asynchronous method to perform the main logic.
        """
        self.logger.info("Starting host process.")

        # Run the Auchan order scraping process
        await self.auchan_order_service.scrape_auchan_order_history()

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