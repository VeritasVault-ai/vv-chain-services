from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List


@dataclass_json
@dataclass
class AssetViewResult:
    Asset: List[str]
    Weights: List[float]

@dataclass_json
@dataclass
class ViewResult:
    Weights: List[AssetViewResult]
    Confidence: float
    Return: float


@dataclass_json
@dataclass
class AllocationResult:
    asset: str
    weight: float


@dataclass_json
@dataclass
class ModelResult:
    Views: List[ViewResult]
    Allocations: List[AllocationResult]


@dataclass_json
@dataclass
class BlackLittermanModelResults:
    Model: str
    Submodel: str
    ModelResults: List[ModelResult]
