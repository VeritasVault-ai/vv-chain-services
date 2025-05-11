from typing import List
import numpy as np
import pandas as pd
from pypfopt.black_litterman import BlackLittermanModel, market_implied_risk_aversion
from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData
from pypfopt import risk_models, expected_returns
from pypfopt.efficient_frontier import EfficientFrontier
from main_app.data_classes.BlackLittermanModelResult import BlackLittermanModelResults, ModelResult, Allocation, View


class ViewGenerator:
    def __init__(self, indexes: List[str], apy_data: pd.DataFrame):
        self._indexes = indexes
        self._apy_data = apy_data


    def calculate(self) -> List[pd.Series]:
        # Extract data
        apy_data = self._apy_data

        # Calculate historical returns and covariance
        mu = expected_returns.mean_historical_return(apy_data)

        # Step 2: Create non-ML views (simple momentum + valuation signals)
        momentum = apy_data.pct_change(90).iloc[-1]  # 3-month momentum
        valuation = 1 / mu  # crude valuation proxy: inverse historical return

        # Combine into views
        momentum_per_view = [0.4, 0.5, 0.6]
        views = [m * momentum + (1 - m) * valuation for m in momentum_per_view]
        views = views / np.linalg.norm(views) * 0.05  # scale to ~5% target return

        return views


class BlackLittermanYieldModel:
    def __init__(self, model_data: BlackLittermanModelData):
        self.model_data = model_data

        self._indexes = ["{}.{}.{}".format(datum.Chain, datum.Pool, datum.Project) for datum in model_data.CryptoMarketData]
        self._apy_data = pd.DataFrame([[metric.APY for metric in datum.Metrics] for datum in model_data.CryptoMarketData], index=self._indexes)
        self._tvl_data = pd.DataFrame([[metric.TVL for metric in datum.Metrics] for datum in model_data.CryptoMarketData], index=self._indexes)

        self.view_generator = ViewGenerator(model_data.CryptoMarketData)

    def calculate(self) -> BlackLittermanModelResults:
        indexes = self._indexes
        apy_data = self._apy_data
        tvl_data = self._tvl_data

        # Calculate historical returns and covariance
        mu = expected_returns.mean_historical_return(apy_data)
        S = risk_models.sample_cov(apy_data)

        # Step 1: Compute equilibrium market returns (CAPM-implied)
        tvl = self._tvl_data.iloc[-1]
        tvl_series = pd.Series(tvl, index=indexes)
        delta = market_implied_risk_aversion(tvl_data.iloc[-1])  # ~2.5–3 by default
        prior = delta * S @ tvl_series / tvl_series.sum()

        # Create uncertainty (more signal → lower variance)
        views = self.view_generator.calculate()

        model_results = []
        for view in views:
            confidence = np.abs(view) / view.abs().max()
            omega = np.diag((1 - confidence + 0.05))  # add small floor for stability

            # Step 3: Apply Black-Litterman model
            bl = BlackLittermanModel(S, pi=prior, absolute_views=view, omega=omega)
            bl_return = bl.bl_returns()
            bl_cov = bl.bl_cov()

            # Step 4: Get portfolio weights
            ef = EfficientFrontier(bl_return, bl_cov)
            # weights = ef.max_sharpe()
            cleaned_weights = ef.clean_weights()

            view_result = [View(v.Weights, v.Return) for v in view]
            allocations = [Allocation(w.index, w) for w in cleaned_weights]
            model_results.append(ModelResult(Views=view_result, Allocations=allocations))

        return BlackLittermanModelResults(
            Model="BlackLittermanModel",
            ModelResults=model_results)