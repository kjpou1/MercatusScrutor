from dataclasses import dataclass

@dataclass
class CommandLineArgs:
    scraping_interval: int  # Interval for scraping in minutes
    target_url: str  # URL to scrape
    headless: bool  # Whether to run the browser in headless mode
    username: str  # Username for login
    password: str  # Password for login