using System;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace VeritasVault.Risk.Event
{
    /// <summary>
    /// Models for blockchain events received from Goldsky
    /// </summary>
    
    // Incoming blockchain event from Goldsky
    public class BlockchainEvent
    {
        [JsonProperty("vaultId")]
        public string VaultId { get; set; }
        
        [JsonProperty("network")]
        public string Network { get; set; }
        
        [JsonProperty("eventType")]
        public string EventType { get; set; }
        
        [JsonProperty("timestamp")]
        public DateTime Timestamp { get; set; }
        
        [JsonProperty("collateralAssets")]
        public List<CollateralAsset> CollateralAssets { get; set; }
        
        [JsonProperty("debtAssets")]
        public List<DebtAsset> DebtAssets { get; set; }
        
        [JsonProperty("transactionHash")]
        public string TransactionHash { get; set; }
    }

    public class CollateralAsset
    {
        [JsonProperty("assetId")]
        public string AssetId { get; set; }
        
        [JsonProperty("amount")]
        public decimal Amount { get; set; }
        
        [JsonProperty("price")]
        public decimal Price { get; set; }
        
        [JsonProperty("liquidationThreshold")]
        public decimal LiquidationThreshold { get; set; }
    }

    public class DebtAsset
    {
        [JsonProperty("assetId")]
        public string AssetId { get; set; }
        
        [JsonProperty("amount")]
        public decimal Amount { get; set; }
        
        [JsonProperty("price")]
        public decimal Price { get; set; }
        
        [JsonProperty("interestRate")]
        public decimal InterestRate { get; set; }
    }
}