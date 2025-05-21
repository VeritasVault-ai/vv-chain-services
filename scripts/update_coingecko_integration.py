#!/usr/bin/env python3
"""
CoinGecko Integration Update Script
This script handles updating and synchronizing data from CoinGecko API.
"""

import os
import sys
import json
import time
import logging
import requests
import stat
from datetime import datetime

# Constants
JSON_INDENT = 2
DEFAULT_TOP_COINS_LIMIT = 250
DEFAULT_PAGE = 1
REQUEST_TIMEOUT = 30
API_VERSION = "1.0.0"
ERROR_EXIT_CODE = 1

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("coingecko-integration")

# Configuration
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
COINGECKO_API_KEY = os.environ.get("COINGECKO_API_KEY", "")
if not COINGECKO_API_KEY:
    logger.warning("COINGECKO_API_KEY not set - running in free tier mode with rate limits")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "coingecko")

def get_headers():
    """
    Returns HTTP headers for CoinGecko API requests, including an API key if set.
    """
    headers = {
        "Accept": "application/json"
    }
    if COINGECKO_API_KEY:
        headers["X-CG-Pro-API-Key"] = COINGECKO_API_KEY
    return headers

def respect_rate_limits(response):
    """Check response headers and respect rate limits"""
    remaining = response.headers.get('X-RateLimit-Remaining')
    try:
        remaining = int(response.headers.get("X-RateLimit-Remaining", "999"))
    except ValueError:
        remaining = 999
    if remaining < 5:
        reset_after = response.headers.get("X-RateLimit-Reset")
    if reset_after and reset_after.isdigit():
        sleep_time = int(reset_after) + 1          # header is already “seconds to reset”
    if remaining and int(remaining) < 5:
        reset_time = response.headers.get('X-RateLimit-Reset')
        if reset_time:
            sleep_time = max(int(reset_time) - time.time(), 0) + 1
            logger.info(f"Rate limit approaching, sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)
        else:
            logger.info("Rate limit approaching, sleeping for 10 seconds")
            time.sleep(10)
    else:
        # Add a small delay between requests regardless
        time.sleep(0.5)

def fetch_coins_list():
    """
    Fetches the complete list of coins from the CoinGecko API and saves it to a local JSON file.

    Returns:
        The list of coins as parsed from the API response, or None if the request fails.
    """
    url = f"{COINGECKO_API_BASE}/coins/list"
    logger.info(f"Fetching coins list from {url}")

    try:
        response = requests.get(url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        respect_rate_limits(response)
        coins = response.json()

        # Save to file
        output_file = os.path.join(DATA_DIR, "coins_list.json")
        with open(output_file, "w") as f:
            json.dump(coins, f, indent=JSON_INDENT)
        os.chmod(output_file, stat.S_IRUSR | stat.S_IWUSR)

        logger.info(f"Saved {len(coins)} coins to {output_file}")
        return coins
    except Exception as e:
        logger.error(
            f"Error fetching coins list: {str(e)}, "
            f"Status Code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}, "
            f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}, "
            f"URL: {url}"
        )
        return None

def fetch_global_data():
    """
    Fetches global cryptocurrency market data from the CoinGecko API.

    Retrieves overall market statistics, saves the data to 'global.json' in the data directory,
    and returns the parsed JSON data. Returns None if the request fails.
    """
    url = f"{COINGECKO_API_BASE}/global"
    logger.info(f"Fetching global market data from {url}")

    try:
        response = requests.get(url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        respect_rate_limits(response)
        global_data = response.json()

        # Save to file
        output_file = os.path.join(DATA_DIR, "global.json")
        with open(output_file, "w") as f:
            json.dump(global_data, f, indent=JSON_INDENT)

        logger.info(f"Saved global market data to {output_file}")
        return global_data
    except Exception as e:
        logger.error(
            f"Error fetching global data: {str(e)}, "
            f"Status Code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}, "
            f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}, "
            f"URL: {url}"
        )
        return None

def fetch_top_coins(limit=DEFAULT_TOP_COINS_LIMIT):
    """
    Fetches detailed market data for the top cryptocurrencies by market capitalization.

    Retrieves market data for the top `limit` coins from the CoinGecko API, including price change
    percentages over 1 hour, 24 hours, and 7 days. Saves the resulting data to a JSON file in the
    data directory. Returns the data as a list of dictionaries, or None if the request fails.

    Args:
        limit: The number of top coins to fetch (default is DEFAULT_TOP_COINS_LIMIT).

    Returns:
        A list of dictionaries containing market data for each coin, or None on failure.
    """
    url = f"{COINGECKO_API_BASE}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": DEFAULT_PAGE,
        "sparkline": False,
        "price_change_percentage": "1h,24h,7d"
    }

    logger.info(f"Fetching top {limit} coins from {url}")

    try:
        response = requests.get(url, headers=get_headers(), params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        respect_rate_limits(response)
        top_coins = response.json()

        # Save to file
        output_file = os.path.join(DATA_DIR, f"top_{limit}_coins.json")
        with open(output_file, "w") as f:
            json.dump(top_coins, f, indent=JSON_INDENT)

        logger.info(f"Saved top {len(top_coins)} coins to {output_file}")
        return top_coins
    except Exception as e:
        logger.error(
            f"Error fetching top coins: {str(e)}, "
            f"Status Code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}, "
            f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}, "
            f"URL: {url}"
        )
        return None

def fetch_categories():
    """Fetch cryptocurrency categories"""
    url = f"{COINGECKO_API_BASE}/coins/categories"
    logger.info(f"Fetching categories from {url}")

    try:
        response = requests.get(url, headers=get_headers(), timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        respect_rate_limits(response)
        categories = response.json()

        # Save to file
        output_file = os.path.join(DATA_DIR, "categories.json")
        with open(output_file, "w") as f:
            json.dump(categories, f, indent=JSON_INDENT)

        logger.info(f"Saved {len(categories)} categories to {output_file}")
        return categories
    except Exception as e:
        logger.error(
            f"Error fetching categories: {str(e)}, "
            f"Status Code: {e.response.status_code if hasattr(e, 'response') else 'N/A'}, "
            f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}, "
            f"URL: {url}"
        )
        return None

def update_metadata():
    """Update metadata file with timestamp and version info"""
    metadata = {
        "last_updated": datetime.utcnow().isoformat(),
        "version": API_VERSION,
        "api_base": COINGECKO_API_BASE
    }

    output_file = os.path.join(DATA_DIR, "metadata.json")
    with open(output_file, "w") as f:
        json.dump(metadata, f, indent=JSON_INDENT)
    os.chmod(output_file, stat.S_IRUSR | stat.S_IWUSR)

    logger.info(f"Updated metadata at {output_file}")

def main():
    """
    Coordinates the full update process for CoinGecko data, including fetching all datasets,
    saving them locally, updating metadata, and logging progress.

    Exits the program with status ERROR_EXIT_CODE if any data fetch fails.
    """
    logger.info("Starting CoinGecko integration update")
    start_time = time.time()

    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)

    # Fetch all required data
    success = all([
        fetch_coins_list() is not None,
        fetch_global_data() is not None,
        fetch_top_coins() is not None,
        fetch_categories() is not None
    ])

    if not success:
        logger.error("One or more operations failed")
        sys.exit(ERROR_EXIT_CODE)

    # Update metadata
    update_metadata()

    elapsed_time = time.time() - start_time
    logger.info(f"CoinGecko integration update completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
