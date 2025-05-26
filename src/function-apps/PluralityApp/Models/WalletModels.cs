using System;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace VeritasVault.Plurality.Models
{
    /// <summary>
    /// Models for wallet integration via Plurality
    /// </summary>
    
    // Request to connect a wallet
    public class WalletConnectionRequest
    {
        [JsonProperty("walletAddress")]
        public string WalletAddress { get; set; }
        
        [JsonProperty("walletType")]
        public string WalletType { get; set; }
        
        [JsonProperty("chainId")]
        public string ChainId { get; set; }
        
        [JsonProperty("signature")]
        public string Signature { get; set; }
        
        [JsonProperty("message")]
        public string Message { get; set; }
        
        [JsonProperty("timestamp")]
        public long TimestampUnix { get; set; }
    }

    // Response for wallet connection
    public class WalletConnectionResponse
    {
        [JsonProperty("connectionId")]
        public string ConnectionId { get; set; }
        
        [JsonProperty("walletAddress")]
        public string WalletAddress { get; set; }
        
        [JsonProperty("status")]
        public string Status { get; set; }
        
        [JsonProperty("message")]
        public string Message { get; set; }
        
        [JsonProperty("timestamp")]
        public DateTime Timestamp { get; set; }
    }

    // Wallet transaction request
    public class WalletTransactionRequest
    {
        [JsonProperty("connectionId")]
        public string ConnectionId { get; set; }
        
        [JsonProperty("walletAddress")]
        public string WalletAddress { get; set; }
        
        [JsonProperty("transactionType")]
        public string TransactionType { get; set; }
        
        [JsonProperty("transactionData")]
        public string TransactionData { get; set; }
        
        [JsonProperty("chainId")]
        public string ChainId { get; set; }
        
        [JsonProperty("timestamp")]
        public long TimestampUnix { get; set; }
    }

    // Wallet transaction response
    public class WalletTransactionResponse
    {
        [JsonProperty("transactionId")]
        public string TransactionId { get; set; }
        
        [JsonProperty("status")]
        public string Status { get; set; }
        
        [JsonProperty("message")]
        public string Message { get; set; }
        
        [JsonProperty("transactionHash")]
        public string TransactionHash { get; set; }
        
        [JsonProperty("timestamp")]
        public DateTime Timestamp { get; set; }
    }

    // Wallet status model
    public class WalletStatus
    {
        [JsonProperty("connectionId")]
        public string ConnectionId { get; set; }
        
        [JsonProperty("walletAddress")]
        public string WalletAddress { get; set; }
        
        [JsonProperty("walletType")]
        public string WalletType { get; set; }
        
        [JsonProperty("chainId")]
        public string ChainId { get; set; }
        
        [JsonProperty("isConnected")]
        public bool IsConnected { get; set; }
        
        [JsonProperty("lastActivity")]
        public DateTime LastActivity { get; set; }
        
        [JsonProperty("verificationStatus")]
        public string VerificationStatus { get; set; }
    }

    // Plurality verification request
    public class PluralityVerificationRequest
    {
        [JsonProperty("walletAddress")]
        public string WalletAddress { get; set; }
        
        [JsonProperty("chainId")]
        public string ChainId { get; set; }
        
        [JsonProperty("verificationLevel")]
        public string VerificationLevel { get; set; }
        
        [JsonProperty("timestamp")]
        public long TimestampUnix { get; set; }
    }

    // Plurality verification response
    public class PluralityVerificationResponse
    {
        [JsonProperty("verificationId")]
        public string VerificationId { get; set; }
        
        [JsonProperty("status")]
        public string Status { get; set; }
        
        [JsonProperty("message")]
        public string Message { get; set; }
        
        [JsonProperty("verificationUrl")]
        public string VerificationUrl { get; set; }
        
        [JsonProperty("expiresAt")]
        public DateTime ExpiresAt { get; set; }
    }

    // Wallet balance model
    public class WalletBalance
    {
        [JsonProperty("walletAddress")]
        public string WalletAddress { get; set; }
        
        [JsonProperty("chainId")]
        public string ChainId { get; set; }
        
        [JsonProperty("assets")]
        public List<AssetBalance> Assets { get; set; }
        
        [JsonProperty("timestamp")]
        public DateTime Timestamp { get; set; }
    }

    public class AssetBalance
    {
        [JsonProperty("assetId")]
        public string AssetId { get; set; }
        
        [JsonProperty("symbol")]
        public string Symbol { get; set; }
        
        [JsonProperty("amount")]
        public decimal Amount { get; set; }
        
        [JsonProperty("valueUsd")]
        public decimal ValueUsd { get; set; }
    }
}

