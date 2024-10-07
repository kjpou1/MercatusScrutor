# MercatusScrutor

MercatusScrutor is a web scraping tool specifically designed to automate the extraction and analysis of order data from Auchan Drive. It enables users to efficiently track, store, and update information about their supermarket purchases. With built-in capabilities to manage historical order records, the tool focuses on ensuring that all orders are tracked, avoiding redundant processing and providing insightful details about purchases. MercatusScrutor emphasizes reliability, scalability, and optimized performance for the seamless handling of large amounts of order data.

The name "MercatusScrutor" has Latin roots, where "Mercatus" means marketplace, and "Scrutor" means to search or examine thoroughly, reflecting the tool's purpose of efficiently examining marketplace order data.

## Table of Contents

- [MercatusScrutor](#mercatusscrutor)
  - [Table of Contents](#table-of-contents)
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
    - [Adding This to the README](#adding-this-to-the-readme)
    - [Running the Container with Automatic Restart](#running-the-container-with-automatic-restart)
    - [Check Logs](#check-logs)
    - [Stop the Container](#stop-the-container)
  - [Shell Script](#shell-script)
    - [Shell Script Examples](#shell-script-examples)
    - [Running the Shell Script](#running-the-shell-script)
  - [License](#license)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/kjpou1/MercatusScrutor.git
    cd project_name
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

5. **Set environment file**

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

# Time interval (in minutes) between each scraping process
SCRAPING_INTERVAL=30

# Target URL to start scraping from
TARGET_URL=https://auchandrive.lu/historique-commandes

# Run the browser in headless mode (true/false)
HEADLESS=false

# Username for logging into the Auchan Drive account
USERNAME=your_username_here

# Password for logging into the Auchan Drive account
PASSWORD=your_password_here

# Path to the order history file
ORDER_HISTORY_FILE=./data/order_history.json
```

> [!NOTE]
> Headless mode must be set to `true` if running on a Raspberry Pi.
> An `example_env` file is provided to get started. Copy the file to `.env` before running:

Yes, you can configure Docker to automatically restart the container if it stops or if the host machine reboots. This is done using the `--restart` policy or by specifying it in `docker-compose.yml`. The `unless-stopped` restart policy ensures that the container will restart automatically unless it is explicitly stopped.

Here’s how you can set it up:

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

### Adding This to the README

Here’s how to add the automatic restart information to the `README.md`:

```markdown
## Docker

### Docker Setup

To containerize and run MercatusScrutor using Docker, follow these steps:

1. **Create the `.env` file** as described in the [Configuration](#configuration) section and ensure that it is listed in `.gitignore` to avoid committing sensitive information to version control.

### Building the Docker Image

You can build the Docker image using the `Dockerfile` provided in the project root:

```bash
docker build -t mercatusscrutor .
```

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

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
