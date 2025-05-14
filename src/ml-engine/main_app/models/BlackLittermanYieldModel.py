from typing import List
import numpy as np
import pandas as pd
from pypfopt.black_litterman import BlackLittermanModel, market_implied_risk_aversion
from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData
from pypfopt import risk_models, expected_returns
from pypfopt.efficient_frontier import EfficientFrontier
from main_app.data_classes.BlackLittermanModelResult import BlackLittermanModelResults, ModelResult, Allocation, View, \
    AssetWeights
from main_app.infrastructure.defi_llama import get_historic_tvl_and_apy_from_symbol


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
        period = 30
        momentum = apy_data.iloc[0] / apy_data.iloc[period] - 1 # 1-month momentum
        valuation = 1 / mu  # crude valuation proxy: inverse historical return

        # Combine into views
        momentum_per_view = [0.4, 0.5, 0.6]
        views = [
            ((m * momentum + (1 - m) * valuation)
             .pipe(lambda s: 0.05 * s / np.linalg.norm(s)))
            for m in momentum_per_view
        ]
        return views


class BlackLittermanYieldModel:
    def __init__(self, model_data: BlackLittermanModelData):
        self.model_data = model_data

        self._indexes = [datum.Symbol.upper() for datum in model_data.CryptoMarketData]
        if not self._indexes:
            raise ValueError("No crypto market data provided")

        # If we have been passed market data, use it, else retrieve.
        # The assumption is that if we haven't been passed market data for the first asset then we don't have for the
        # rest. todo make clear in interface / amend implementation
        if model_data.CryptoMarketData[0].Metrics is not None and len(model_data.CryptoMarketData[0].Metrics) != 0:
            raise Exception("Custom market data not supported at present")
        else:
            self._apy_data = pd.DataFrame()
            self._tvl_data = pd.DataFrame()
            
            for symbol in self._indexes:
                df = get_historic_tvl_and_apy_from_symbol(symbol)
                
                # we only use the last value each day for model purposes to reduce noise
                df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.date
                df = df.groupby("timestamp").last()

                # Sort by descending date and only include the last 365 days
                df = df.sort_index(ascending=False)
                df = df.iloc[:365]

                self._apy_data[symbol] = df["apy"] / 100
                self._tvl_data[symbol] = df["tvlUsd"]

            
            self._apy_data.fillna(method="bfill", inplace=True)
            self._tvl_data.fillna(method="bfill", inplace=True)

        if self._apy_data.empty or self._tvl_data.empty:
            raise ValueError("Missing APY or TVL data")

        self.view_generator = ViewGenerator(self._indexes, self._apy_data)

    def calculate(self) -> BlackLittermanModelResults:
        indexes = self._indexes
        apy_data = self._apy_data
        tvl_data = self._tvl_data

        # Calculate historical returns and covariance
        S = risk_models.sample_cov(apy_data)

        # Step 1: Compute equilibrium market returns (CAPM-implied)
        tvl = tvl_data.iloc[0]
        tvl_series = pd.Series(tvl, index=indexes)
        delta = market_implied_risk_aversion(apy_data.iloc[0])  # ~2.5–3 by default
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
            weights = ef.max_sharpe()  # Uncomment this or choose another optimization objective
            cleaned_weights = ef.clean_weights()
            view_result = [
                View(
                    Weights=[AssetWeights(str(asset), float(view[asset]))],
                    Return=float(ret),
                )
                for asset, ret in view.items()
            ]
            allocations = [
                Allocation(asset, weight)
                for asset, weight in cleaned_weights.items()
            ]
            model_results.append(ModelResult(Views=view_result, Allocations=allocations))

        return BlackLittermanModelResults(
            Model="BlackLittermanModel",
            ModelResults=model_results)