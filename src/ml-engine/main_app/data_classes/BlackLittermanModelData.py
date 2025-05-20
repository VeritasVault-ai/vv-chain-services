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
    Timestamp: str
    TVL: float
    APY: float
    Base_APY: Optional[float] = field(default=None)
    Reward_APY: Optional[float] = field(default=None)


@dataclass_json
@dataclass
class AssetStaticData:
    Pool: Optional[str]
    Project: Optional[str]
    Chain: Optional[str]
    Symbol: str

@dataclass_json
@dataclass
class ExplicitReturnView:
    Symbols: List[str]
    Weights: List[float]
    ExpectedReturn: float
    Confidence: float


@dataclass_json
@dataclass
class BlackLittermanModelData:
    Model: str
    Submodel: str
    AssetSymbols: List[str]
    ModelParameters: ModelParameters
    RiskFreeRates: Optional[List[RiskFreeRate]]
    PortfolioViews: Optional[List[ExplicitReturnView]]
    AssetStaticData: List[AssetStaticData] = field(default=None)