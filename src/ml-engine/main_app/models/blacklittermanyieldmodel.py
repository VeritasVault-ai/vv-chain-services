from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData
from typing import List


class BlackLittermanYieldModel:
    def __init__(self, model_data: BlackLittermanModelData):
        self.model_data = model_data

    def calculate(self) -> List['BlackLittermanYieldModelResult']:
        pass


class BlackLittermanYieldModelResult:
    """
    Represents the results of a Black-Litterman model calculation.

    Attributes:
        views: List of views on expected returns
        allocations: List of recommended asset allocations
    """
    def __init__(self, views: List[float], allocations: List[float]):
        self.views = views
        self.allocations = allocations