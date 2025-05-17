#!/usr/bin/env python3
"""
DefiLlama Integration Update Script
This script handles updating and synchronizing data from DefiLlama API.
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
logger = logging.getLogger("defillama-integration")

# Configuration
DEFILLAMA_API_BASE = "https://api.llama.fi"
DEFILLAMA_API_KEY = os.environ.get("DEFILLAMA_API_KEY", "")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "defillama")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def get_headers():
    """Get headers for API requests with authentication if available"""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    if DEFILLAMA_API_KEY:
        headers["Authorization"] = f"Bearer {DEFILLAMA_API_KEY}"
    return headers

def fetch_protocols():
    """Fetch all protocols from DefiLlama"""
    url = f"{DEFILLAMA_API_BASE}/protocols"
    logger.info(f"Fetching protocols from {url}")
    
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        protocols = response.json()
        
        # Save to file
        output_file = os.path.join(DATA_DIR, "protocols.json")
        with open(output_file, "w") as f:
            json.dump(protocols, f, indent=2)
        
        logger.info(f"Saved {len(protocols)} protocols to {output_file}")
        return protocols
    except Exception as e:
        logger.error(f"Error fetching protocols: {e}")
        return None

def fetch_tvl_data():
    """Fetch TVL data from DefiLlama"""
    url = f"{DEFILLAMA_API_BASE}/charts"
    logger.info(f"Fetching TVL data from {url}")
    
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        tvl_data = response.json()
        
        # Save to file
        output_file = os.path.join(DATA_DIR, "tvl.json")
        with open(output_file, "w") as f:
            json.dump(tvl_data, f, indent=2)
        
        logger.info(f"Saved TVL data to {output_file}")
        return tvl_data
    except Exception as e:
        logger.error(f"Error fetching TVL data: {e}")
        return None

def fetch_chains():
    """Fetch chains data from DefiLlama"""
    url = f"{DEFILLAMA_API_BASE}/chains"
    logger.info(f"Fetching chains data from {url}")
    
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        chains_data = response.json()
        
        # Save to file
        output_file = os.path.join(DATA_DIR, "chains.json")
        with open(output_file, "w") as f:
            json.dump(chains_data, f, indent=2)
        
        logger.info(f"Saved chains data to {output_file}")
        return chains_data
    except Exception as e:
        logger.error(f"Error fetching chains data: {e}")
        return None

def update_metadata():
    """Update metadata file with timestamp and version info"""
    metadata = {
        "last_updated": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "api_base": DEFILLAMA_API_BASE
    }
    
    output_file = os.path.join(DATA_DIR, "metadata.json")
    with open(output_file, "w") as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Updated metadata at {output_file}")

def main():
    """Main function to update all DefiLlama data"""
    logger.info("Starting DefiLlama integration update")
    start_time = time.time()
    
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Fetch all required data
    fetch_protocols()
    fetch_tvl_data()
    fetch_chains()
    
    # Update metadata
    update_metadata()
    
    elapsed_time = time.time() - start_time
    logger.info(f"DefiLlama integration update completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()