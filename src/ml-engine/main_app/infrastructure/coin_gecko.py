import time
from typing import Dict
import requests
import json
from defi_llama import get_pool_summary_data


def get_coin_list():
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data


def get_contract_addresses(symbol_chain_map: Dict[str, str], timeout: int = 10, retries: int = 3) -> Dict[str, str]:
    contract_addresses = {}

    def safe_request(url: str, retries: int, timeout: int):
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=timeout)

                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 2 ** attempt + 10))
                    print(f"Rate limited. Waiting {retry_after} seconds before retrying...")
                    time.sleep(retry_after)
                    continue

                response.raise_for_status()
                return response

            except requests.Timeout:
                wait = 3 ** attempt
                print(f"Timeout on {url}. Retrying in {wait} seconds...")
                time.sleep(wait)

            except requests.RequestException as e:
                if response := getattr(e, "response", None):
                    if response.status_code == 429:
                        retry_after = int(response.headers.get("Retry-After", 2 ** attempt))
                        print(f"Rate limited. Waiting {retry_after} seconds before retrying...")
                        time.sleep(retry_after)
                        continue
                raise e
        raise requests.Timeout("Max retries exceeded or rate limited too often.")

    for symbol, chain in symbol_chain_map.items():
        chain = chain.lower()
        try:
            print(f"Processing {symbol.upper()} on {chain.capitalize()}...")

            # Step 1: Search by symbol
            search_url = f'https://api.coingecko.com/api/v3/search?query={symbol}'
            search_response = safe_request(search_url, retries, timeout)
            coins = search_response.json().get('coins', [])

            # Step 2: Find coin ID match
            coin_id = None
            for coin in coins:
                if coin['symbol'].lower() == symbol.lower():
                    coin_id = coin['id']
                    break

            if not coin_id:
                contract_addresses[symbol] = "Symbol not found"
                continue

            # Step 3: Get platform contract info
            detail_url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
            detail_response = safe_request(detail_url, retries, timeout)
            platforms = detail_response.json().get('platforms', {})

            address = platforms.get(chain)
            if address:
                contract_addresses[symbol] = f"{chain}:{address}"
                print(f"{symbol.upper()}: {chain}:{address}")
            else:
                contract_addresses[symbol] = f"No contract on {chain}"

        except requests.Timeout:
            contract_addresses[symbol] = "Timeout after retries"
        except requests.RequestException as e:
            contract_addresses[symbol] = f"Request error: {str(e)}"
        except Exception as e:
            contract_addresses[symbol] = f"Unexpected error: {str(e)}"

    return contract_addresses


def save_to_json(data: Dict[str, str], filename: str = "contract_addresses.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n✅ Results saved to {filename}")


if __name__ == "__main__":
    pool_data = get_pool_summary_data()

    COINGECKO_CHAIN_MAP = {
        'Ethereum': 'ethereum',
        'Solana': 'solana',
        'Move': None,  # Not a platform, rather a language
        'Tron': 'tron',
        'BSC': 'binance-smart-chain',
        'Base': 'base',
        'Avalanche': 'avalanche',
        'Polygon': 'polygon-pos',
        'Sonic': None,  # Unknown
        'Aptos': 'aptos',
        'Core': 'core',
        'Filecoin': 'filecoin',
        'Arbitrum': 'arbitrum-one',
        'Cronos': 'cronos',
        'Berachain': None,  # Not on CoinGecko yet
        'Sui': 'sui',
        'Gnosis': 'xdai',
        'Bitcoin': 'bitcoin',
        'Venom': None,  # Not found
        'Polkadot': 'polkadot',
        'Cardano': 'cardano',
        'Flare': 'flare-network',
        'MultiversX': 'elrond',
        'Sei': 'sei',
        'Bob': None,  # Unknown
        'Hemi': None,  # Unknown
        'Stacks': 'stacks',
        'Kava': 'kava',
        'Gravity': None,  # Ambiguous
        'Fuel-ignition': None,  # Not present
        'Icp': 'internet-computer',
        'Celo': 'celo',
        'Optimism': 'optimistic-ethereum',
        'Ton': 'the-open-network',
        'Starknet': 'starknet',
        'Tezos': 'tezos',
        'Fraxtal': None,  # Very new, likely not yet supported
        'Algorand': 'algorand',
        'Op_bnb': 'op-bnb',
        'Neutron': 'neutron',
        'Doge': 'dogecoin',
        'Bitcoincash': 'bitcoin-cash',
        'Linea': 'linea',
        'Mantle': 'mantle',
        'zkSync Era': 'zksync',
        'Litecoin': 'litecoin',
        'Swellchain': None,  # Unknown
        'APTOS': 'aptos',
        'Metis': 'metis-andromeda',
        'Etherlink': 'etherlink',
        'Blast': 'blast',
        'Osmosis': 'osmosis',
        'Rootstock': 'rootstock',
        'Manta': 'manta',
        'Ontology': 'ontology',
        'Kusama': 'kusama',
        'Neo': 'neo',
        'Waves': 'waves',
        'Bifrost Network': 'bifrost',
        'Moonbeam': 'moonbeam',
        'Fantom': 'fantom',
        'Chiliz': 'chiliz',
        'Astar': 'astar',
        'Acala': 'acala',
        'Polygon zkEVM': 'polygon-zkevm',
        'Klaytn': 'klay-token',
        'ICP': 'internet-computer',
        'Telos': 'telos',
        'Defichain': 'defichain',
        'Polynomial': None,  # Unclear what chain this refers to
        'Mixin': 'mixin-network',
        'Cosmos': 'cosmos',
        'Bifrost': 'bifrost',
        'Moonriver': 'moonriver',
        'Karura': 'karura',
        'Cronos_zkevm': None,  # Not a known CoinGecko key
        'Stellar': 'stellar',
        'Conflux': 'conflux',
        'Canto': 'canto',
        'Aurora': 'aurora',
        'Heco': 'huobi-token',
        'Unit0': None,  # Unknown
        'Scroll': 'scroll',
        'Persistence': 'persistence',
        'Carbon': 'carbon',
        'LightLink': None,  # Unknown
        'Kujira': 'kujira',
        'Neon': 'neon-evm',
        'Xdc': 'xdce-crowd-sale',
        'Vechain': 'vechain',
        'AO': None,  # Unknown
        'Obyte': 'byteball',
        'Zksync': 'zksync',
        'Mode': 'mode',
        'Re.al': None,  # Not found
        'IOTA EVM': 'iota-evm',
        'Libre': None,  # Not found
        'Bsquared': None,  # Not found
        'Rollux': 'rollux'
    }

    symbol_to_chain = {key: COINGECKO_CHAIN_MAP[value[0].chain] for key, value in pool_data.items() \
                       if COINGECKO_CHAIN_MAP[value[0].chain] is not None and not '-' in key}

    result = get_contract_addresses(symbol_to_chain)
    for symbol, address in result.items():
        print(f"{symbol.upper()}: {address}")
    save_to_json(result)