using System;
using System.Linq;
using VeritasVault.RiskBotApp.Models;

namespace VeritasVault.RiskBotApp
{
    public static class Helpers
    {
        /// <summary>
        /// Maps the blockchain event to the format expected by the ML service
        /// </summary>
        public static RiskPredictionRequest MapToRiskPredictionRequest(BlockchainEvent blockchainEvent)
        {
            var request = new RiskPredictionRequest
            {
                VaultId = blockchainEvent.VaultId,
                Network = blockchainEvent.Network,
                TimestampUnix = ((DateTimeOffset)blockchainEvent.Timestamp).ToUnixTimeSeconds(),
                Collateral = blockchainEvent.CollateralAssets?.Select(asset => new CollateralItem
                {
                    AssetId = asset.AssetId,
                    Amount = asset.Amount,
                    ValueUsd = asset.Amount * asset.Price,
                    LiquidationThreshold = asset.LiquidationThreshold
                }).ToList(),
                Debt = blockchainEvent.DebtAssets?.Select(asset => new DebtItem
                {
                    AssetId = asset.AssetId,
                    Amount = asset.Amount,
                    ValueUsd = asset.Amount * asset.Price,
                    InterestRate = asset.InterestRate
                }).ToList()
            };
            
            return request;
        }
        
        /// <summary>
        /// Maps the ML service response to the Redis storage model
        /// </summary>
        public static VaultMetrics MapToVaultMetrics(RiskPrediction prediction, string eventId)
        {
            return new VaultMetrics
            {
                Ltv = prediction.Ltv,
                Tvl = prediction.Tvl,
                RiskScore = prediction.RiskScore,
                LiquidationRisk = prediction.LiquidationRisk,
                Timestamp = DateTime.UtcNow,
                EventId = eventId
            };
        }
        
        /// <summary>
        /// Sanitizes input values to prevent invalid data from being processed
        /// </summary>
        public static decimal SanitizeDecimal(decimal value, decimal minValue = 0, decimal maxValue = decimal.MaxValue)
        {
            if (decimal.IsNaN((double)value) || decimal.IsInfinity((double)value))
            {
                return 0;
            }
            
            return Math.Clamp(value, minValue, maxValue);
        }
        
        /// <summary>
        /// Generates a Redis key for storing vault metrics
        /// </summary>
        public static string GenerateVaultMetricsKey(string vaultId, string network)
        {
            return $"vault:{network}:{vaultId}:metrics";
        }
        
        /// <summary>
        /// Generates a Redis key for storing historical vault metrics
        /// </summary>
        public static string GenerateVaultHistoryKey(string vaultId, string network)
        {
            return $"history:{network}:{vaultId}:metrics";
        }
    }
}