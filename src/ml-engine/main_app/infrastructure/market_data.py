from main_app.infrastructure.defi_llama import get_historic_tvl_and_apy_from_pool_id, get_historical_prices, get_pool_summary_data, get_protocol_data
import os
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

def get_historical_data_for_symbol(symbol: str, symbol_to_address_mapping: Dict[str, str],
                                           pools: List[str] = None,
                                           get_protocol_data_flag: bool = False) -> pd.DataFrame:

    """
        Get the combined historical data for a given symbol, including price, TVL, and APY.
        :param symbol: The symbol of the coin (e.g., "ETH").
        :param symbol_to_address_mapping: Dictionary mapping symbols to contract addresses.
        :param pools: List of pool IDs to include in the calculation. If None, all pools for the symbol will be used.
        :param get_protocol_data: If True, includes protocol name, description, and category for each row.
        :return: A pandas DataFrame containing price, TVL, and APY data.
        """

    symbols_lower_map = {key.lower() : key for key in symbol_to_address_mapping.keys()}
    if symbol not in symbols_lower_map:
        raise ValueError(f"Symbol {symbol} not found in mapping.")
    else:
        symbol = symbols_lower_map[symbol]

    contract_address = symbol_to_address_mapping[symbol]
    if 'error' in contract_address.lower():
        raise ValueError(f"Contract address for symbol {symbol} not found.")

    # If pools haven't been specified, load via DefiLlama pool summary
    symbol_to_pools = {}
    if pools is None or get_protocol_data:
        symbol_to_pools = get_pool_summary_data()

    if pools is None:
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

    if get_protocol_data_flag:
        protocol_data_list = get_protocol_data()
        if protocol_data_list:
            # Get pool summary data to match protocol names
            project_names = {p.project.lower() for p in symbol_to_pools[symbol]}

            # Find matching protocol data
            matching_protocol = next(
                (protocol for protocol in protocol_data_list
                 if protocol.name.lower() in project_names),
                None
            )

            if matching_protocol:
                merged_df['protocol_name'] = matching_protocol.name
                merged_df['protocol_description'] = matching_protocol.description
                merged_df['protocol_category'] = matching_protocol.category
            else:
                merged_df['protocol_name'] = ''
                merged_df['protocol_description'] = ''
                merged_df['protocol_category'] = ''

    return merged_df


def get_enriched_pool_summary_data() -> pd.DataFrame:
    """
    Get pool summary data enriched with protocol information.

    Returns:
        pd.DataFrame: A DataFrame containing pool summary data with added protocol information.
    """

    symbol_to_pools = get_pool_summary_data()
    protocol_data_list = get_protocol_data()
    protocol_data_map = {protocol.name.lower() : protocol for protocol in protocol_data_list}

    enriched_data = {}
    for symbol, pools in symbol_to_pools.items():
        matching_protocols = [ p.project.lower() in protocol_data_map and protocol_data_map[p.project.lower()] or None for p in pools]
        if matching_protocols:
            for i in range(len(pools)):
                if matching_protocols[i] is not None:
                    pools[i].protocolName = matching_protocols[i].name
                    pools[i].protocolDescription = matching_protocols[i].description
                    pools[i].protocolCategory = matching_protocols[i].category
                    pools[i].protocolData = matching_protocols[i]

        enriched_data[symbol] = pools

    # Convert to DataFrame
    rows = []
    for symbol, pools in enriched_data.items():
        for pool in pools:
            row = {
                'symbol': symbol,
                'pool': pool.pool,
                'project': pool.project,
                'chain': pool.chain,
                'tvl': pool.tvlUsd,
                'apy': pool.apy,
                'protocol_name': pool.protocolName,
                'protocol_description': pool.protocolDescription,
                'protocol_category': pool.protocolCategory
            }
            rows.append(row)

    return pd.DataFrame(rows)


if __name__ == "__main__":
    symbol = "steth"
    mapping_file_path = "../../static_data/symbol_to_contract_address_map.json"

    # Test both functions
    symbol_to_address_mapping = load_symbol_to_address_mapping(mapping_file_path)
    df = get_historical_data_for_symbol(symbol, symbol_to_address_mapping, None, True)
    print("Historical data:")
    print(df.head())

    enriched_pools_df = get_enriched_pool_summary_data()
    print("\nEnriched pool summary data:")
    print(enriched_pools_df.head())