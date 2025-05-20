import numpy as np
import pandas as pd
from pypfopt.black_litterman import BlackLittermanModel, market_implied_risk_aversion
from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData
from pypfopt import risk_models
from pypfopt.efficient_frontier import EfficientFrontier
from main_app.data_classes.BlackLittermanModelResults import BlackLittermanModelResults, ModelResult, AllocationResult, ViewResult, \
    AssetViewResult
from main_app.infrastructure.defi_llama import get_historic_tvl_and_apy_from_symbol
from main_app.models.black_litterman.BlExplicitReturnViewGenerator import BlExplicitReturnViewGenerator


class BlPortfolioModel:
    def __init__(self, model_data: BlackLittermanModelData):
        """
        Initializes the Black-Litterman portfolio model with market data.
        
        Constructs asset identifiers, APY, and TVL data frames from the provided model data. Raises a ValueError if required market data is missing. Instantiates a ViewGenerator for generating views based on the APY data.
        """
        self._model_data = model_data
        self._indexes = model_data.AssetSymbols

        self._apy_data = pd.DataFrame()
        self._tvl_data = pd.DataFrame()

        # get market data
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

        # Create a view generator used to create views to be consumed by the model
        self.view_generator = BlExplicitReturnViewGenerator(self._indexes, self._apy_data, self._model_data.PortfolioViews)

    def calculate(self) -> BlackLittermanModelResults:
        """
        Runs the Black-Litterman portfolio optimization using APY and TVL data.
        
        Calculates the sample covariance and equilibrium market returns, generates multiple views based on momentum and valuation signals, and applies the Black-Litterman model to adjust expected returns and covariances. For each view, optimizes the portfolio for maximum Sharpe ratio and aggregates the resulting views and allocations into model results.
        
        Returns:
            BlackLittermanModelResults: The results of the Black-Litterman optimization, including per-view portfolio allocations and view details.
        """
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

        confidence = np.diag([v.Confidence for v in views])
        omega = np.diag((1 - np.diagonal(confidence) + 0.05))  # add small floor for stability

        # Step 3: Apply Black-Litterman model
        picking_matrix = [v.Weights for v in views] # picking matrix of weights
        return_vector = np.array([v.ExpectedReturn for v in views])
        bl = BlackLittermanModel(S, pi=prior, omega=omega, P=picking_matrix, Q=return_vector)
        bl_return = bl.bl_returns()
        bl_cov = bl.bl_cov()

        # Step 4: Get portfolio weights
        ef = EfficientFrontier(bl_return, bl_cov)
        weights = ef.max_sharpe()  # Uncomment this or choose another optimization objective
        cleaned_weights = ef.clean_weights()
        view_result = [
            ViewResult(
                Weights=[AssetViewResult(indexes, list(view.Weights))],
                Return=view.ExpectedReturn,
                Confidence=view.Confidence
            )
            for view in views
        ]
        allocations = [
            AllocationResult(asset, weight)
            for asset, weight in cleaned_weights.items()
        ]
        model_results.append(ModelResult(Views=view_result, Allocations=allocations))

        return BlackLittermanModelResults(
            Model=self._model_data.Model,
            Submodel=self._model_data.Submodel,
            ModelResults=model_results)