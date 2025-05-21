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
from datetime import datetime

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
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "coingecko")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def get_headers():
    """Get headers for API requests with authentication if available"""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    if COINGECKO_API_KEY:
        headers["X-CG-Pro-API-Key"] = COINGECKO_API_KEY
    return headers

def fetch_coins_list():
    """Fetch list of all coins from CoinGecko"""
    url = f"{COINGECKO_API_BASE}/coins/list"
    logger.info(f"Fetching coins list from {url}")
    
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        coins = response.json()
        
        # Save to file
        output_file = os.path.join(DATA_DIR, "coins_list.json")
        with open(output_file, "w") as f:
            json.dump(coins, f, indent=2)
        
        logger.info(f"Saved {len(coins)} coins to {output_file}")
        return coins
    except Exception as e:
        logger.error(f"Error fetching coins list: {e}")
        return None

def fetch_global_data():
    """Fetch global cryptocurrency market data"""
    url = f"{COINGECKO_API_BASE}/global"
    logger.info(f"Fetching global market data from {url}")
    
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        global_data = response.json()
        
        # Save to file
        output_file = os.path.join(DATA_DIR, "global.json")
        with open(output_file, "w") as f:
            json.dump(global_data, f, indent=2)
        
        logger.info(f"Saved global market data to {output_file}")
        return global_data
    except Exception as e:
        logger.error(f"Error fetching global market data: {e}")
        return None

def fetch_top_coins(limit=250):
    """Fetch top coins by market cap with detailed data"""
    url = f"{COINGECKO_API_BASE}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "1h,24h,7d"
    }
    
    logger.info(f"Fetching top {limit} coins from {url}")
    
    try:
        response = requests.get(url, headers=get_headers(), params=params)
        response.raise_for_status()
        top_coins = response.json()
        
        # Save to file
        output_file = os.path.join(DATA_DIR, f"top_{limit}_coins.json")
        with open(output_file, "w") as f:
            json.dump(top_coins, f, indent=2)
        
        logger.info(f"Saved top {len(top_coins)} coins to {output_file}")
        return top_coins
    except Exception as e:
        logger.error(f"Error fetching top coins: {e}")
        return None

def fetch_categories():
    """Fetch cryptocurrency categories"""
    url = f"{COINGECKO_API_BASE}/coins/categories"
    logger.info(f"Fetching categories from {url}")
    
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        categories = response.json()
        
        # Save to file
        output_file = os.path.join(DATA_DIR, "categories.json")
        with open(output_file, "w") as f:
            json.dump(categories, f, indent=2)
        
        logger.info(f"Saved {len(categories)} categories to {output_file}")
        return categories
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        return None

def update_metadata():
    """Update metadata file with timestamp and version info"""
    metadata = {
        "last_updated": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "api_base": COINGECKO_API_BASE
    }
    
    output_file = os.path.join(DATA_DIR, "metadata.json")
    with open(output_file, "w") as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Updated metadata at {output_file}")

def main():
    """Main function to update all CoinGecko data"""
    logger.info("Starting CoinGecko integration update")
    start_time = time.time()
    
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Fetch all required data
    success = True
    success = fetch_coins_list() is not None and success
    success = fetch_global_data() is not None and success
    success = fetch_top_coins(250) is not None and success
    success = fetch_categories() is not None and success
    
    if not success:
        logger.error("One or more operations failed")
        sys.exit(1)
    
    # Update metadata
    update_metadata()
    
    elapsed_time = time.time() - start_time
    logger.info(f"CoinGecko integration update completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()