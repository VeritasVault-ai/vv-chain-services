from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List


@dataclass_json
@dataclass
@dataclass_json
@dataclass
class AssetWeights:
    Asset: str  # Capitalize to match other classes
    Weight: float

@dataclass_json
@dataclass
class View:
    Weights: List[AssetWeights]
    Return: float


@dataclass_json
@dataclass
class Allocation:
    asset: str
    weight: float


@dataclass_json
@dataclass
class ModelResult:
    Views: List[View]
    Allocations: List[Allocation]


@dataclass_json
@dataclass
class BlackLittermanModelResults:
    Model: str
    ModelResults: List[ModelResult]
