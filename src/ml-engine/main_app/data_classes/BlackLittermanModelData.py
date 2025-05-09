from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Optional


@dataclass_json
@dataclass
class ModelParameters:
    RiskAversion: Optional[float] = field(default=2.5)
    UncertaintyInPrior: Optional[float] = field(default=0.05)


@dataclass_json
@dataclass
class RiskFreeRate:
    term: str
    rate: float


@dataclass_json
@dataclass
class Metrics:
    Date: str
    TVL: float
    APY: float
    Base_APY: Optional[float] = field(default=None)
    Reward_APY: Optional[float] = field(default=None)


@dataclass_json
@dataclass
class CryptoMarketData:
    Pool: str
    Project: str
    Chain: str
    Metrics: List[Metrics]


@dataclass_json
@dataclass
class BlackLittermanModelData:
    Model: str
    ModelParameters: ModelParameters
    RiskFreeRates: List[RiskFreeRate]
    CryptoMarketData: List[CryptoMarketData]