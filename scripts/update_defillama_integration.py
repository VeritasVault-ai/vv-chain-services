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

# Constants
JSON_INDENT = 2
REQUEST_TIMEOUT = 30
API_VERSION = "1.0.0"
ERROR_EXIT_CODE = 1

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
    """
    Returns HTTP headers for DefiLlama API requests, including authentication if an API key is set.

    If the DEFILLAMA_API_KEY environment variable is present, adds a bearer token for authenticated requests.
    """
    headers = {
        "Accept": "application/json"
    }
    if DEFILLAMA_API_KEY:
        headers["Authorization"] = f"Bearer {DEFILLAMA_API_KEY}"
    return headers

def fetch_and_save_data(endpoint, filename, data_description):
    """Generic function to fetch data from DefiLlama API and save it to a file"""
    url = f"{DEFILLAMA_API_BASE}/{endpoint}"
    logger.info(f"Fetching {data_description} from {url}")

    try:
        response = requests.get(url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        # Save to file
        output_file = os.path.join(DATA_DIR, filename)
        with open(output_file, "w") as f:
            json.dump(data, f, indent=JSON_INDENT)
        os.chmod(output_file, stat.S_IRUSR | stat.S_IWUSR)

        logger.info(f"Saved {data_description} to {output_file}")
        return data
    except requests.exceptions.RequestException:
        logger.exception(f"Network error while fetching {data_description}")
        return None
    except json.JSONDecodeError:
        logger.exception(f"Failed to decode JSON response from {data_description} API")
        return None
    except IOError:
        logger.exception(f"Failed to write {data_description} to {output_file}")
        return None
    except Exception:
        logger.exception(f"Unexpected error while fetching {data_description}")
        return None

def fetch_protocols():
    """Fetch all protocols from DefiLlama"""
    protocols = fetch_and_save_data("protocols", "protocols.json", "protocols")
    if protocols:
        logger.info(f"Fetched {len(protocols)} protocols")
    return protocols

def fetch_tvl_data():
    """Fetch TVL data from DefiLlama"""
    return fetch_and_save_data("charts", "tvl.json", "TVL data")

def fetch_chains():
    """Fetch chains data from DefiLlama"""
    return fetch_and_save_data("chains", "chains.json", "chains data")

def update_metadata():
    """  
    The metadata file is saved in the data directory with user read/write permissions.
    """
    output_file = os.path.join(DATA_DIR, "metadata.json")
    metadata = {
        "last_updated": datetime.utcnow().isoformat(),
        "version": API_VERSION,
        "api_base": DEFILLAMA_API_BASE
    }

    try:
        with open(output_file, "w") as f:
            json.dump(metadata, f, indent=JSON_INDENT)
        os.chmod(output_file, stat.S_IRUSR | stat.S_IWUSR)
        logger.info(f"Updated metadata at {output_file}")
    except IOError as e:
        logger.exception(f"Failed to write metadata to {output_file}, Error: {str(e)}")

def main():
    """
    Coordinates the full DefiLlama data update process, including data fetching and metadata refresh.
    
    Creates the data directory if needed, retrieves protocols, TVL, and chains data from the DefiLlama API, saves them locally, updates metadata, and logs progress. Exits with an error if any data fetch fails.
    """
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
        sys.exit(ERROR_EXIT_CODE)
    
    # Update metadata
    update_metadata()
    
    elapsed_time = time.time() - start_time
    logger.info(f"DefiLlama integration update completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
