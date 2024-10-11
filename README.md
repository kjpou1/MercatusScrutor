# MercatusScrutor

MercatusScrutor is a web scraping tool, powered by **Playwright**, designed to automate the extraction and analysis of order data from Auchan Drive. It enables users to efficiently track, store, and update information about their supermarket purchases. The tool integrates with **Grocy**, an open-source home management system, to automate inventory updates based on your orders, ensuring real-time synchronization of your stock with minimal manual intervention.

With built-in capabilities to manage historical order records, MercatusScrutor focuses on ensuring that all orders are tracked, avoiding redundant processing, and providing insightful details about purchases. By leveraging **cosine similarity** for product matching and TTL (Time-to-Live) caching for API efficiency, the tool emphasizes reliability, scalability, and optimized performance for handling large amounts of order data.

The name "MercatusScrutor" has Latin roots, where "Mercatus" means marketplace, and "Scrutor" means to search or examine thoroughly, reflecting the tool's purpose of efficiently examining marketplace order data.

## Table of Contents

- [MercatusScrutor](#mercatusscrutor)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Features](#features)
  - [Grocy Integration](#grocy-integration)
    - [Grocy Integration Features](#grocy-integration-features)
    - [Cosine Similarity in Matching](#cosine-similarity-in-matching)
    - [Example Workflow with Grocy](#example-workflow-with-grocy)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Command Line Arguments](#command-line-arguments)
    - [Examples](#examples)
  - [Configuration](#configuration)
    - [Example `.env` file:](#example-env-file)
    - [Using Docker Compose](#using-docker-compose)
      - [Example `docker-compose.yml`:](#example-docker-composeyml)
    - [Using Docker Command](#using-docker-command)
      - [Example Command:](#example-command)
    - [Explanation of the `--restart` Policies:](#explanation-of-the---restart-policies)
    - [Running the Container with Automatic Restart](#running-the-container-with-automatic-restart)
    - [Check Logs](#check-logs)
    - [Stop the Container](#stop-the-container)
  - [Shell Script](#shell-script)
    - [Shell Script Examples](#shell-script-examples)
    - [Running the Shell Script](#running-the-shell-script)
  - [Contributing](#contributing)
  - [Known Issues / Limitations](#known-issues--limitations)
  - [Future Roadmap](#future-roadmap)
  - [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.x
- Docker (for containerization)
- Git (for cloning the repository)
- A valid Grocy API setup (if using the inventory feature)

Here’s an example that includes both the **existing features** and the **newly highlighted ones** for a more comprehensive **Features** section:

## Features

- **Efficient Caching for API Calls**  
  Reduce unnecessary API requests with TTL (Time-to-Live) caching of products and locations. This optimization helps improve performance by reducing the load on the Grocy API and making the tool more scalable. Cache durations are configurable via environment variables.

- **Live Stock Updates**  
  Optionally enable real-time updates to the Grocy stock whenever new orders are processed. This ensures that your inventory remains up-to-date with minimal manual intervention. The live stock update feature can be toggled on or off via the `LIVE_STOCK_UPDATE` environment variable.

- **Product Matching with Cosine Similarity**  
  Ensure accurate product matching between the order data and your Grocy inventory using cosine similarity. This algorithm improves the precision of product matching, helping avoid mismatches, especially when dealing with large or similar product sets.

- **Customizable Product Matching Thresholds**  
  Set your own similarity thresholds to control how closely products need to match to be processed. Additionally, configure a warning threshold to log near matches, providing flexibility for different levels of matching precision.

- **Automatic Scraping of Auchan Drive Orders**  
  Automate the extraction of order data from Auchan Drive. The tool tracks historical orders, ensuring that redundant orders are skipped, and only new or updated orders are processed, streamlining data handling.

- **Historical Order Tracking**  
  Store and track historical order data in a JSON file. This enables better management of recurring orders and allows for easy reference to past purchases.

- **Docker Support for Easy Deployment**  
  Deploy the tool effortlessly with Docker. Utilize the `docker-compose.yml` for containerization, with support for automatic restarts and environment variable configurations to ensure the tool runs reliably across environments.

- **Configurable Settings via `.env`**  
  Customize scraping intervals, API base URLs, product matching thresholds, and other critical settings via a simple `.env` file. This allows for easy configuration changes without altering the codebase.

## Grocy Integration

MercatusScrutor integrates with **Grocy**, an open-source home management system, to automate inventory management based on your Auchan Drive orders. This integration ensures that your Grocy stock remains synchronized with real-world purchases.

### Grocy Integration Features

- **Automatic Stock Updates**  
  MercatusScrutor can automatically update Grocy’s stock for matching products from your Auchan Drive orders. Products are added to the correct stock location with the proper quantities and prices based on the order data.

- **Cosine Similarity-Based Product Matching**  
  To match products between Auchan Drive orders and your Grocy inventory, MercatusScrutor uses **cosine similarity**, a mathematical algorithm that compares the similarity between two sets of text data. This helps ensure accurate product matching even if the product names aren't an exact match. The similarity threshold can be customized in the `.env` file to control how strict the matching should be.

- **Configurable Matching Thresholds**  
  Set the threshold for product similarity using cosine similarity to match the product names between Auchan Drive orders and Grocy inventory. Configure a secondary warning threshold to log near matches for review.

- **Real-Time Updates**  
  With the `LIVE_STOCK_UPDATE` setting enabled, Grocy stock is updated in real-time. Alternatively, you can turn this off for batch updates later.

- **Location Matching**  
  MercatusScrutor supports mapping products to custom locations within Grocy. For example, if your Grocy inventory has items stored in a location labeled “Parking,” MercatusScrutor will ensure the order data is matched to that location.

---

### Cosine Similarity in Matching

MercatusScrutor relies on the **cosine similarity** algorithm to match product names between Auchan Drive orders and Grocy inventory items. Cosine similarity measures the angle between two vectors in a multi-dimensional space, where the vectors represent text strings (such as product names). This approach works well for comparing similar or near-identical product names, even if they have minor differences in formatting or spelling.

By default, products that meet or exceed the configured similarity threshold (e.g., 90%) are considered matches, and stock updates are applied to these products. Products that fall between the warning threshold and the similarity threshold trigger warnings in the logs, allowing users to review potential near-matches manually.

---

### Example Workflow with Grocy

1. **Scraping**: MercatusScrutor scrapes the order history from Auchan Drive.
2. **Matching**: It uses cosine similarity to match products from the orders with existing Grocy products.
3. **Stock Update**: If live updates are enabled, the matching products are immediately added to your Grocy stock.
4. **Caching**: Products and locations are cached for a set duration to optimize API calls.


## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/kjpou1/MercatusScrutor.git
    cd MercatusScrutor
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set environment file**

    Copy or rename the `example_env` file to `.env` before running:

    ```bash
    cp example_env .env
    ```

## Usage

To run the library, use the provided `run.py` script with appropriate command-line arguments.

### Command Line Arguments

To run the script, you can pass command-line arguments to override environment settings. These arguments include:
- `--scraping-interval`: Time interval (in minutes) between each scraping run.
- `--target-url`: Target URL for scraping.
- `--headless`: Run the browser in headless mode (true/false).
  > **Note**: Headless mode must be set to `true` if running on a Raspberry Pi.
- `--username`: Username for logging into Auchan Drive.
- `--password`: Password for logging into Auchan Drive.

### Examples

To run the program with default settings:

```bash
python run.py
```

To run the program with custom command-line arguments:

```bash
python run.py --scraping-interval 60 --target-url https://custom-url.com --headless --username myemail@example.com --password mypassword
```

## Configuration

The configuration settings are managed through environment variables and can be set in a `.env` file in the root directory of the project.

### Example `.env` file:

```bash
# Example .env file for MercatusScrutor

# Time interval (in minutes) between each scraping process.
# This defines how frequently the tool will check for new orders.
# Example: SCRAPING_INTERVAL=30 will scrape every 30 minutes.
SCRAPING_INTERVAL=30

# The target URL from which to scrape order history.
# This is the URL of the Auchan Drive order history page.
# Example: TARGET_URL=https://auchandrive.lu/historique-commandes
TARGET_URL=https://auchandrive.lu/historique-commandes

# Whether to run the browser in headless mode (true/false).
# Headless mode means the browser will run without a visible window.
# Note: Headless must be set to 'true' if running on a Raspberry Pi.
# Example: HEADLESS=true
HEADLESS=false

# The username for logging into your Auchan Drive account.
# This should be the email address or username used for login.
# Example: USERNAME=myemail@example.com
USERNAME=your_username_here

# The password for logging into your Auchan Drive account.
# This should be the password associated with your Auchan Drive account.
# Example: PASSWORD=mysecretpassword
PASSWORD=your_password_here

# The file path where the order history will be saved.
# This is the location where the tool will save a JSON file containing
# the historical order data.
# Example: ORDER_HISTORY_FILE=./data/order_history.json
ORDER_HISTORY_FILE=order_history.json  

# The base URL for the Grocy API.
# This is the API endpoint for your Grocy installation, which should be
# the URL of the server where Grocy is hosted.
# Example: GROCY_API_BASE=http://homeassistant.local:9192
GROCY_API_BASE=http://homeassistant.local:9192

# The API key for accessing the Grocy API.
# This key is required for authentication to interact with the Grocy API.
# Ensure this key is stored securely and not shared publicly.
# Example: GROCY_API_KEY=your_api_key_here
GROCY_API_KEY=your_api_key_here

# The similarity threshold for matching products in Grocy.
# Products with a similarity percentage below this value will not be processed.
# Example: SIMILARITY_THRESHOLD=90 means products must match with at least 90% similarity.
SIMILARITY_THRESHOLD=90

# Warning similarity threshold for logging warnings.
# Products with a similarity percentage equal to or greater than this value 
# but below the SIMILARITY_THRESHOLD will trigger a warning in the logs.
# Example: WARNING_SIMILARITY_THRESHOLD=75 will trigger warnings for matches >= 75% but < 90%.
WARNING_SIMILARITY_THRESHOLD=75

# Live stock update flag (true/false).
# If set to true, the system will automatically update Grocy stock with
# matching products from the order. If set to false, stock updates will be skipped.
# Example: LIVE_STOCK_UPDATE=true will enable live stock updates.
LIVE_STOCK_UPDATE=false

```

> **Note**: Headless mode must be set to `true` if running on a Raspberry Pi.

### Using Docker Compose

In your `docker-compose.yml`, you can specify the `restart: unless-stopped` policy to make sure the container restarts automatically unless you explicitly stop it.

#### Example `docker-compose.yml`:

```yaml
version: '3.8'
services:
  mercatusscrutor:
    build: .
    container_name: mercatusscrutor
    env_file:
      - .env  # Load environment variables from the .env file
    volumes:
      - ./data:/app/data  # Map the local data directory
    restart: unless-stopped  # Restart the container unless manually stopped
```

### Using Docker Command

If you're not using Docker Compose and are running the container directly with the `docker run` command, you can use the `--restart unless-stopped` flag.

#### Example Command:
```bash
docker run -d --env-file .env -v $(pwd)/data:/app/data --restart unless-stopped mercatusscrutor
```

### Explanation of the `--restart` Policies:

1. **`no`**: The container will not be restarted if it stops.
2. **`always`**: The container will always restart if it stops or if Docker itself restarts.
3. **`on-failure`**: The container will restart only if it exits with a non-zero exit code (i.e., if it crashes).
4. **`unless-stopped`**: The container will restart unless it was explicitly stopped by the user (e.g., with `docker stop`).

### Running the Container with Automatic Restart

To run the container and ensure it restarts automatically unless explicitly stopped, use Docker Compose:

```bash
docker-compose up --build -d
```

Alternatively, if you are using plain Docker, run:

```bash
docker run -d --env-file .env -v $(pwd)/data:/app/data --restart unless-stopped mercatusscrutor
```

- `--restart unless-stopped`: Ensures the container automatically restarts unless it is explicitly stopped by the user.
- `--env-file .env`: Loads environment variables from the `.env` file.
- `-v $(pwd)/data:/app/data`: Maps the local `./data` directory to the container.

### Check Logs

To check the logs and verify that the scraping process is running:

```bash
docker logs mercatusscrutor
```

### Stop the Container

To stop the running container:

```bash
docker-compose down
```

> **Note**: Stopping the container will prevent it from restarting automatically until you start it again manually.

## Shell Script

A shell script `run.sh` is provided to automate the execution of the script.

### Shell Script Examples

Example `run.sh`

```bash
#!/bin/bash
source ./.venv/bin/activate
python ./run.py
deactivate
```

### Running the Shell Script

To run the script and clear the directory before running:

```bash
./run.sh
```

## Contributing

We welcome contributions! Here's how you can help:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## Known Issues / Limitations

- Currently, only orders with a similarity above the threshold are added to stock

.
- The tool assumes the Grocy API is fully operational and accessible at all times.
- Live stock updates may increase API calls; use with caution in high-traffic systems.

## Future Roadmap

- Add support for other supermarket scraping sources.
- Implement more granular stock management features.
- Expand error handling and retries for scraping and API calls.
- Enable scheduled runs with dynamic business hours.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

