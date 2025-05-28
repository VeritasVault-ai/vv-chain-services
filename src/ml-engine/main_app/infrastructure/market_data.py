from main_app.infrastructure.defi_llama import get_historic_tvl_and_apy_from_pool_id, get_historical_prices, get_pool_summary_data
import json
import pandas as pd
from typing import List, Dict
from datetime import date

def load_symbol_to_address_mapping(file_path: str) -> dict[str, str]:
    """
    Load the mapping of symbols to contract addresses from a JSON file.
    :param file_path: Path to the JSON file.
    :return: A dictionary mapping symbols to contract addresses.
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def get_historical_data_for_symbol(symbol: str, symbol_to_address_mapping: Dict[str,str], pools: List[str] = None) -> pd.DataFrame:
    """
    Get the combined historical data for a given symbol, including price, TVL, and APY.
    :param symbol: The symbol of the coin (e.g., "ETH").
    :param symbol_to_address_mapping: Dictionary mapping symbols to contract addresses.
    :param pools: List of pool IDs to include in the calculation. If None, all pools for the symbol will be used.
    :return: A pandas DataFrame containing price, TVL, and APY data.

    """

    if symbol not in symbol_to_address_mapping:
        raise ValueError(f"Symbol {symbol} not found in mapping.")

    contract_address = symbol_to_address_mapping[symbol]
    if 'error' in contract_address.lower():
        raise ValueError(f"Contract address for symbol {symbol} not found.")

    # If pools haven't been specified, load via DefiLlama pool summary
    if pools is None:
        symbol_to_pools = get_pool_summary_data()
        pools = [p.pool for p in symbol_to_pools[symbol]]

    # Get pool summary data and their corresponding historic TVL and APY
    tvl_apy_data = []
    for pool_id in pools:
        tvl_apy_data.append(get_historic_tvl_and_apy_from_pool_id(pool_id))
    
    # Calculate total TVL and weighted average APY for each date
    combined_tvl_apy = pd.DataFrame()
    for df in tvl_apy_data:
        combined_tvl_apy = pd.concat([combined_tvl_apy, df])

    combined_tvl_apy = combined_tvl_apy.rename(columns={'timestamp': 'date'})
    combined_tvl_apy = combined_tvl_apy.groupby('date').apply(
        lambda x: pd.Series({
            'tvlUsd': x['tvlUsd'].sum(),
            'apy': (x['tvlUsd'] * x['apy']).sum() / x['tvlUsd'].sum() / 100.0
        })
    ).reset_index()

    # Get historical prices for the symbol
    combined_tvl_apy['date'] = pd.to_datetime(combined_tvl_apy['date'])
    start_date = combined_tvl_apy['date'].min()
    end_date = combined_tvl_apy['date'].max()
    price_data = get_historical_prices([contract_address], start_date, end_date)

    # Combine price, TVL, and APY data into a DataFrame
    price_df = pd.DataFrame(price_data[contract_address])
    price_df['date'] = pd.to_datetime(price_df['date']).dt.strftime('%Y-%m-%d')
    combined_tvl_apy['date'] = pd.to_datetime(combined_tvl_apy['date']).dt.strftime('%Y-%m-%d')
    merged_df = pd.merge(price_df, combined_tvl_apy, how='inner', on='date')

    return merged_df


if __name__ == "__main__":
    symbol = "steth"
    mapping_file_path = "static_data/symbol_to_address_map.json"
    symbol_to_address_mapping = load_symbol_to_address_mapping(mapping_file_path)
    df = get_historical_data_for_symbol(symbol, symbol_to_address_mapping)
    print(df.head())