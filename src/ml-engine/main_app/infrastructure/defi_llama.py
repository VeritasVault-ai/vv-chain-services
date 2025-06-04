from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional, Dict

import pandas as pd
import requests


@dataclass
class PoolPredictions:
    binnedConfidence: Optional[float]
    predictedClass: Optional[str]
    predictedProbability: Optional[float]


@dataclass
class ProtocolData:
    id: str
    name: str
    address: Optional[str]
    symbol: Optional[str]
    url: Optional[str]
    description: Optional[str]
    chain: str
    logo: Optional[str]
    audits: Optional[str]
    audit_note: Optional[str]
    gecko_id: Optional[str]
    cmcId: Optional[str]
    category: str
    chains: List[str]
    module: str
    twitter: Optional[str]
    forkedFromIds: List[str]
    oracles: List[str]
    audit_links: List[str]
    listedAt: Optional[int]
    hallmarks: List[List]
    methodology: Optional[str]
    slug: str
    tvl: float
    chainTvls: Dict
    change_1h: Optional[float]
    change_1d: Optional[float]
    change_7d: Optional[float]
    tokenBreakdowns: Dict
    mcap: Optional[float]
    staking: float


@dataclass
class PoolData:
    chain: str
    exposure: str
    ilRisk: str
    outlier: bool
    pool: str
    predictions: PoolPredictions
    project: str
    stableCoin: bool
    symbol: str
    apy: Optional[float]
    apyBase: Optional[float]
    apyBase7d: Optional[float]
    apyBaseInception: Optional[float]
    apyMean30d: Optional[float]
    apyPct1D: Optional[float]
    apyPct30D: Optional[float]
    apyPct7D: Optional[float]
    apyReward: Optional[float]
    count: Optional[int]
    il7d: Optional[float]
    mu: Optional[float]
    poolMeta: Optional[str]
    tvlUsd: Optional[int]
    volumeUsd1d: Optional[float]
    volumeUsd7d: Optional[float]
    sigma: Optional[float]
    protocolName: Optional[str] = None
    protocolDescription: Optional[str]  = None
    protocolCategory: Optional[str]  = None
    protocolData: Optional[ProtocolData] = None
    underlyingTokens: List[str] = field(default_factory=list)
    rewardTokens: List[str] = field(default_factory=list)


def get_pool_summary_data() -> Dict[str, List[PoolData]]:
    url = f"https://yields.llama.fi/pools"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] != "success":
            raise Exception(f"Failed to get pool summary data: DefiLlama return status '{data['status']}'.")

        pools = data['data']
        result = {}
        for pool in pools:
            pool_data = PoolData(
                chain = pool['chain'],
                exposure = pool['exposure'],
                ilRisk = pool['ilRisk'],
                outlier = pool['outlier'],
                pool = pool['pool'],
                predictions = pool['predictions'],
                project = pool['project'],
                stableCoin = pool['stablecoin'],
                symbol = pool['symbol'],
                apy = pool['apy'],
                apyBase = pool['apyBase'],
                apyBase7d = pool['apyBase7d'],
                apyBaseInception = pool['apyBaseInception'],
                apyMean30d = pool['apyMean30d'],
                apyPct1D = pool['apyPct1D'],
                apyPct30D = pool['apyPct30D'],
                apyPct7D = pool['apyPct7D'],
                apyReward = pool['apyReward'],
                count = pool['count'],
                il7d = pool['il7d'],
                mu = pool['mu'],
                poolMeta = pool['poolMeta'],
                tvlUsd = pool['tvlUsd'],
                volumeUsd1d = pool['volumeUsd1d'],
                volumeUsd7d = pool['volumeUsd7d'],
                sigma = pool['sigma'],
                underlyingTokens = pool['underlyingTokens'],
                rewardTokens = pool['rewardTokens']
            )

            symbol = pool_data.symbol
            if symbol in result:
                result[symbol].append(pool_data)
            else:
                result[symbol] = [pool_data]

        return result

    else:
        raise Exception(f"Failed to get pool summary data: {response.status_code} - {response.text}")


def get_pool_ids_from_symbol(symbol: str) -> List[str]:
    summary = get_pool_summary_data()
    # check case-insensitive
    symbol_lower = symbol.lower()
    summary_lower = {key.lower(): key for key in summary.keys()}
    if symbol_lower not in summary_lower:
        raise ValueError(f"Symbol '{symbol}' not found in pool summary data.")
    original_key = summary_lower[symbol_lower]
    ids = [p.pool for p in summary[original_key]]
    return ids


def get_historic_tvl_and_apy_from_pool_id(pool_id) -> pd.DataFrame:
    url = f"https://yields.llama.fi/chart/{pool_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        time_series = data.get("data", [])
        df = pd.DataFrame(time_series)

        return df
    else:
        raise Exception(f"Failed to get historic TVL and APY for {pool_id}: {response.status_code} - {response.text}")


def get_protocol_data() -> List[ProtocolData]:
    url = "https://api.llama.fi/protocols"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        protocols = []
        for protocol in data:
            protocol_data = ProtocolData(
                id=protocol.get('id'),
                name=protocol.get('name'),
                address=protocol.get('address'),
                symbol=protocol.get('symbol'),
                url=protocol.get('url'),
                description=protocol.get('description'),
                chain=protocol.get('chain'),
                logo=protocol.get('logo'),
                audits=protocol.get('audits'),
                audit_note=protocol.get('audit_note'),
                gecko_id=protocol.get('gecko_id'),
                cmcId=protocol.get('cmcId'),
                category=protocol.get('category'),
                chains=protocol.get('chains', []),
                module=protocol.get('module'),
                twitter=protocol.get('twitter'),
                forkedFromIds=protocol.get('forkedFromIds', []),
                oracles=protocol.get('oracles', []),
                audit_links=protocol.get('audit_links', []),
                listedAt=protocol.get('listedAt'),
                hallmarks=protocol.get('hallmarks', []),
                methodology=protocol.get('methodology'),
                slug=protocol.get('slug'),
                tvl=protocol.get('tvl'),
                chainTvls=protocol.get('chainTvls', {}),
                change_1h=protocol.get('change_1h'),
                change_1d=protocol.get('change_1d'),
                change_7d=protocol.get('change_7d'),
                tokenBreakdowns=protocol.get('tokenBreakdowns', {}),
                mcap=protocol.get('mcap'),
                staking=protocol.get('staking', 0)
            )
            protocols.append(protocol_data)
        return protocols
    else:
        raise Exception(f"Failed to get protocol data: {response.status_code} - {response.text}")


def get_historical_prices(coins: list[str], start_date: date, end_date: date) -> dict[str, pd.DataFrame]:
    """
    Fetch daily historical prices from DeFiLlama's /chart/{coin} endpoint.
    
    Args:
        coins (list[str]): List of coin identifiers (e.g., ['ethereum', 'bitcoin']).
        start_date (date): Start date (inclusive).
        end_date (date): End date (inclusive).
    
    Returns:
        dict[str, pd.DataFrame]:
            Mapping from coin to a DataFrame with columns ['date', 'price'], one entry per calendar day.
    """
    base_url = "https://coins.llama.fi/chart/"
    result: dict[str, pd.DataFrame] = {}

    # Build UNIX timestamps at midnight UTC
    start_ts = int(datetime.combine(start_date, datetime.min.time()).timestamp())
    # end_ts   = int(datetime.combine(end_date,   datetime.min.time()).timestamp())

    # Inclusive span in days
    span_days = (end_date - start_date).days + 1

    for coin in coins:
        request = f"{base_url}{coin}?start={start_ts}&period=1d&span={span_days}"
        # request = f"{base_url}{coin}?start={start_ts}&end={end_ts}&span={span_days}&period=1d"
        resp = requests.get(request)
        if resp.status_code != 200:
            print(f"Error fetching {coin}: {resp.status_code} - {resp.text}")
            continue

        prices = resp.json().get("coins", {}).get(coin, {}).get("prices", [])
        # Filter milliseconds‐timestamps to [start_ts, end_ts]
        filtered = [
            {"date": pd.to_datetime(entry['timestamp'], unit='s', utc=True), "price": entry['price']}
            for entry in prices
        ]

        # Convert to DataFrame and limit to one entry per day, up to span_days
        result[coin] = pd.DataFrame(filtered)

    return result


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

