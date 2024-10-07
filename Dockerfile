# Use the official Python image as a base
FROM python:3.9-slim

# Install required system dependencies for Chromium
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    wget \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements first for caching purposes
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and only Chromium browser
RUN pip install playwright && playwright install chromium

# Copy the rest of the application code
COPY . .

# Create the ./data directory if it doesn't exist
RUN mkdir -p ./data

# Expose the data directory for external mapping
VOLUME [ "/app/data" ]

# Set environment variables for production
ENV PYTHONUNBUFFERED=1

# Specify the entrypoint (this is the script that will be run)
CMD ["python", "run.py"]
