using System;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace VeritasVault.Risk.Domain
{
    /// <summary>
    /// Domain models for risk prediction and ML service integration
    /// </summary>
    
    // Request to ML service
    public class RiskPredictionRequest
    {
        [JsonProperty("vaultId")]
        public string VaultId { get; set; }
        
        [JsonProperty("network")]
        public string Network { get; set; }
        
        [JsonProperty("collateral")]
        public List<CollateralItem> Collateral { get; set; }
        
        [JsonProperty("debt")]
        public List<DebtItem> Debt { get; set; }
        
        [JsonProperty("timestamp")]
        public long TimestampUnix { get; set; }
    }

    public class CollateralItem
    {
        [JsonProperty("assetId")]
        public string AssetId { get; set; }
        
        [JsonProperty("amount")]
        public decimal Amount { get; set; }
        
        [JsonProperty("valueUsd")]
        public decimal ValueUsd { get; set; }
        
        [JsonProperty("liquidationThreshold")]
        public decimal LiquidationThreshold { get; set; }
    }

    public class DebtItem
    {
        [JsonProperty("assetId")]
        public string AssetId { get; set; }
        
        [JsonProperty("amount")]
        public decimal Amount { get; set; }
        
        [JsonProperty("valueUsd")]
        public decimal ValueUsd { get; set; }
        
        [JsonProperty("interestRate")]
        public decimal InterestRate { get; set; }
    }

    // Response from ML service
    public class RiskPrediction
    {
        [JsonProperty("ltv")]
        public decimal Ltv { get; set; }
        
        [JsonProperty("tvl")]
        public decimal Tvl { get; set; }
        
        [JsonProperty("riskScore")]
        public decimal? RiskScore { get; set; }
        
        [JsonProperty("liquidationRisk")]
        public string LiquidationRisk { get; set; }
    }
    
    // Redis storage model
    public class VaultMetrics
    {
        [JsonProperty("ltv")]
        public decimal Ltv { get; set; }
        
        [JsonProperty("tvl")]
        public decimal Tvl { get; set; }
        
        [JsonProperty("riskScore")]
        public decimal? RiskScore { get; set; }
        
        [JsonProperty("liquidationRisk")]
        public string LiquidationRisk { get; set; }
        
        [JsonProperty("timestamp")]
        public DateTime Timestamp { get; set; }
        
        [JsonProperty("eventId")]
        public string EventId { get; set; }
    }
}