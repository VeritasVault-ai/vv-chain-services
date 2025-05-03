from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData
from typing import List


class BlackLittermanYieldModel:
    def __init__(self, model_data: BlackLittermanModelData):
        self.model_data = model_data

    def calculate(self) -> List['BlackLittermanYieldModelResult']:
        pass


class BlackLittermanYieldModelResult:
    def __init__(self, views: List, allocations: List):
        pass