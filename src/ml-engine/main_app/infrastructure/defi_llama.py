import requests
import pandas as pd

def get_pool_summary():
    url = f"https://yields.llama.fi/pools"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pools = data.get("data", [])

        # Convert to dictionary mapping symbol to data (grouping values for repeated symbols)
        symbol_to_data = {}

        for item in pools:
            symbol = item['symbol']
            if symbol in symbol_to_data:
                symbol_to_data[symbol].append(item)
            else:
                symbol_to_data[symbol] = [item]

        return symbol_to_data

    else:
        raise Exception(f"Failed to get pool summary data: {response.status_code} - {response.text}")


def get_historic_tvl_and_apy_from_pool_id(pool_id):
    url = f"https://yields.llama.fi/chart/{pool_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get("data", [])
        df = pd.DataFrame(time_series)

        return df
    else:
        raise Exception(f"Failed to get historic TVL and APY for {pool_id}: {response.status_code} - {response.text}")


def get_historic_tvl_and_apy_from_symbol(symbol):
    pool_map =  {
                    "STETH": "747c1d2a-c668-4682-b9f9-296708a3dd90",
                    "GHO": "ff2a68af-030c-4697-b0a1-b62a738eaef0",
                    "USDC": "aa70268e-4b52-42bf-a116-608b370f9501",
                    "WBTC": "d4b3c522-6127-4b89-bedf-83641cdcd2eb",
                    "JITOSOL": "0e7d0722-9054-4907-8593-567b353c0900"
                }

    normalized_symbol = symbol.upper()
    if normalized_symbol not in pool_map:
        raise ValueError(
            f"Symbol '{symbol}' not found in pool mapping. Available symbols: " + ', '.join(pool_map.keys()))

    return get_historic_tvl_and_apy_from_pool_id(pool_map[normalized_symbol])



if __name__ == "__main__":
    # Example usage
    symbols = ["WBTC"]
    for symbol in symbols:
        df = get_historic_tvl_and_apy_from_symbol(symbol)
        print(df.head())