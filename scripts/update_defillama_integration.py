#!/usr/bin/env python3
"""
DefiLlama Integration Update Script
This script handles updating and synchronizing data from DefiLlama API.
"""

import os
import sys
import json
import time
import stat
import logging
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("defillama-integration")

# Configuration
DEFILLAMA_API_BASE = "https://api.llama.fi"
DEFILLAMA_API_KEY = os.environ.get("DEFILLAMA_API_KEY", "")
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "defillama"
)


def get_headers():
    """Get headers for API requests, including authentication if API key is available.

    Authentication increases rate limits and enables access to premium features.
    Set DEFILLAMA_API_KEY environment variable to enable authentication.

    Returns:
        dict: Headers with content-type and optional authentication token."""
    headers = {
        "Accept": "application/json"
    }
    if DEFILLAMA_API_KEY:
        headers["Authorization"] = f"Bearer {DEFILLAMA_API_KEY}"
    return headers


def fetch_data(endpoint, output_filename, data_name="data"):
    """Generic function to fetch data from DefiLlama API

    Args:
        endpoint: API endpoint path (without base URL)
        output_filename: Name of file to save the data
        data_name: Human-readable name for logging purposes

    Returns:
        The fetched data or None if fetch failed
    """
    url = f"{DEFILLAMA_API_BASE}/{endpoint}"
    logger.info(f"Fetching {data_name} from {url}")

    try:
        response = requests.get(url, headers=get_headers(), timeout=30)
        response.raise_for_status()
        data = response.json()

        # Save to file
        output_file = os.path.join(DATA_DIR, output_filename)
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
        os.chmod(output_file, stat.S_IRUSR | stat.S_IWUSR)

        logger.info(f"Saved {data_name} to {output_file}")
        return data
    except requests.exceptions.RequestException:
        logger.exception(f"Network error while fetching {data_name}")
        return None
    except json.JSONDecodeError:
        logger.exception(f"Failed to decode JSON response from {data_name} API")
        return None
    except IOError:
        logger.exception(f"Failed to write {data_name} to {output_file}")
        return None
    except Exception:
        logger.exception(f"Unexpected error while fetching {data_name}")
        return None


def fetch_protocols():
    """Fetch all protocols from DefiLlama"""
    protocols = fetch_data("protocols", "protocols.json", "protocols")
    if protocols:
        logger.info(f"Fetched {len(protocols)} protocols")
    return protocols


def fetch_tvl_data():
    """Fetch TVL data from DefiLlama"""
    return fetch_data("charts", "tvl.json", "TVL data")


def fetch_chains():
    """Fetch chains data from DefiLlama"""
    return fetch_data("chains", "chains.json", "chains data")


def update_metadata():
    """Update metadata file with timestamp and version info"""
    metadata = {
        "last_updated": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "api_base": DEFILLAMA_API_BASE
    }

    output_file = os.path.join(DATA_DIR, "metadata.json")
    try:
        with open(output_file, "w") as f:
            json.dump(metadata, f, indent=2)
        os.chmod(output_file, stat.S_IRUSR | stat.S_IWUSR)
        logger.info(f"Updated metadata at {output_file}")
    except IOError:
        logger.exception(f"Failed to write metadata to {output_file}")


def main():
    """Main function to update all DefiLlama data"""
    logger.info("Starting DefiLlama integration update")
    start_time = time.time()

    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)

    # Fetch all required data
    protocols = fetch_protocols()
    tvl_data = fetch_tvl_data()
    chains = fetch_chains()

    if not all([protocols, tvl_data, chains]):
        logger.error("One or more data fetches failed")
        sys.exit(1)

    # Update metadata
    update_metadata()

    elapsed_time = time.time() - start_time
    logger.info(f"DefiLlama integration update completed in {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()