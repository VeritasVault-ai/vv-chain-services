from typing import List

import numpy as np
import pandas as pd
from pypfopt import expected_returns
from main_app.data_classes.BlackLittermanModelData import ExplicitReturnView


class BlView:
    def __init__(self, weights: pd.Series, confidence: float, expected_return: float):
        self.Weights = weights
        self.Confidence = confidence
        self.ExpectedReturn = expected_return


class BlExplicitReturnViewGenerator:
    def __init__(self, indexes: List[str], asset_market_data: pd.DataFrame = None,
                 portfolio_views_data: List[ExplicitReturnView] = None):
        """
        Initializes the ViewGenerator with asset indexes and APY data.

        Args:
            indexes: List of asset identifiers.
            asset_market_data: DataFrame containing APY data for the assets.
        """
        self._indexes = indexes
        self._asset_market_data = asset_market_data
        self._portfolio_views_data = portfolio_views_data

    def calculate(self) -> List[BlView]:
        # Extract data
        """
        Generates a list of normalized view vectors based on momentum and valuation signals.

        Calculates 3-month momentum and a valuation proxy for each asset, combines them using different weights, normalizes each resulting view, and returns the list of view series.
        """

        if self._portfolio_views_data is None and self._asset_market_data is None:
            raise ValueError("No market data or portfolio views provided. At least market data must be provided.")

        portfolio_views = self._portfolio_views_data
        # at present only contain apy data, this could be extended for other data types
        apy_data = self._asset_market_data

        # Calculate historical returns
        mu = expected_returns.mean_historical_return(apy_data)

        # Case where we have no model data and everything must be calculated from market data
        if portfolio_views is None:
            # Create simple momentum + valuation signals
            period = min(30, len(apy_data) - 1)
            if period <= 0:
                raise ValueError("Not enough history to compute momentum view")

            momentum = 2 * (apy_data.iloc[0] / apy_data.iloc[period] - 1) * 365 / period  # 1-month momentum
            safe_mu = mu.replace(0, np.nan)
            valuation = 0.03 / safe_mu.fillna(safe_mu.mean())  # crude valuation proxy: inverse historical return

            # Combine into views
            m = 0.5
            returns = (m * momentum + (1 - m) * valuation).pipe(lambda s: 0.05 * s / np.linalg.norm(s))
            confidences = [np.abs(ret) / returns.abs().max() for ret in returns]
            weights = pd.Series(1, index=returns.index)
        else:
            returns = [view.ExpectedReturn for view in portfolio_views]
            confidences = [view.Confidence for view in portfolio_views]
            weights = [view.Weights for view in portfolio_views]

        return [BlView(weights=weight, confidence=confidence, expected_return=ret) for \
                    weight, confidence, ret in zip(weights, confidences, returns)]
