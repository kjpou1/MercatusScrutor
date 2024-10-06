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

4. **Set environment file**

    Copy or rename the `example_env` file to `.env` before running

    ```bash
    cp example_env .env
    ```

## Usage

To run the library, use the provided `run.py` script with appropriate command-line arguments.

### Command Line Arguments

The following command-line arguments are supported:

- `--scraping-interval`: Time interval (in minutes) between each scraping process. The default is set to 30 minutes or can be overridden by the `SCRAPING_INTERVAL` environment variable.
  ```bash
  --scraping-interval 45
  ```

- `--target-url`: URL to start scraping from. The default is `https://auchandrive.lu/historique-commandes` or can be overridden by the `TARGET_URL` environment variable.
  ```bash
  --target-url https://custom-url.com
  ```

- `--headless`: Run the browser in headless mode (without a visible browser window). This flag can be set by the `HEADLESS` environment variable (`true` or `false`).
  ```bash
  --headless
  ```

- `--username`: Username for logging into the Auchan Drive account, can be set via the `USERNAME` environment variable.
  ```bash
  --username myemail@example.com
  ```

- `--password`: Password for logging into the Auchan Drive account, can be set via the `PASSWORD` environment variable.
  ```bash
  --password mysecretpassword
  ```

### Examples

To run the program:

```bash
python run.py --scraping-interval 45 --target-url https://custom-url.com --username myemail@example.com --password mysecretpassword --headless
```

## Configuration

The configuration settings are managed through environment variables and can be set in a `.env` file in the root directory of the project.
Example `.env` file:

```
SCRAPING_INTERVAL=30
TARGET_URL=https://auchandrive.lu/historique-commandes
HEADLESS=false
USERNAME=myemail@example.com
PASSWORD=mysecretpassword
```

> [!NOTE]
> An `example_env` file is provided to get started. Copy the file to `.env` before running:

## Shell Script

A shell script `run.sh` is provided to automate the execution of the script.

### Shell Script Examples

Example `run.sh`:

```bash
#!/bin/bash
source ./.venv/bin/activate
python ./run.py --scraping-interval 45 --target-url https://custom-url.com --headless
deactivate
```

### Running the Shell Script

To run the script and clear the directory before running:

```bash
./run.sh
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
