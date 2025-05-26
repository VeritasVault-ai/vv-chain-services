using System;
using System.Collections.Generic;
using Newtonsoft.Json;

namespace VeritasVault.Plurality.Models
{
    /// <summary>
    /// Models for Plurality integration
    /// </summary>
    
    // Plurality API configuration
    public class PluralityConfig
    {
        [JsonProperty("apiUrl")]
        public string ApiUrl { get; set; }
        
        [JsonProperty("apiKey")]
        public string ApiKey { get; set; }
        
        [JsonProperty("apiSecret")]
        public string ApiSecret { get; set; }
        
        [JsonProperty("webhookUrl")]
        public string WebhookUrl { get; set; }
        
        [JsonProperty("verificationLevel")]
        public string VerificationLevel { get; set; }
    }

    // Plurality identity verification
    public class IdentityVerification
    {
        [JsonProperty("verificationId")]
        public string VerificationId { get; set; }
        
        [JsonProperty("userId")]
        public string UserId { get; set; }
        
        [JsonProperty("walletAddress")]
        public string WalletAddress { get; set; }
        
        [JsonProperty("chainId")]
        public string ChainId { get; set; }
        
        [JsonProperty("status")]
        public string Status { get; set; }
        
        [JsonProperty("level")]
        public string Level { get; set; }
        
        [JsonProperty("createdAt")]
        public DateTime CreatedAt { get; set; }
        
        [JsonProperty("updatedAt")]
        public DateTime UpdatedAt { get; set; }
        
        [JsonProperty("expiresAt")]
        public DateTime? ExpiresAt { get; set; }
    }

    // Plurality API response
    public class PluralityApiResponse<T>
    {
        [JsonProperty("success")]
        public bool Success { get; set; }
        
        [JsonProperty("message")]
        public string Message { get; set; }
        
        [JsonProperty("data")]
        public T Data { get; set; }
        
        [JsonProperty("error")]
        public string Error { get; set; }
    }

    // Plurality wallet verification request
    public class PluralityWalletVerificationRequest
    {
        [JsonProperty("walletAddress")]
        public string WalletAddress { get; set; }
        
        [JsonProperty("chainId")]
        public string ChainId { get; set; }
        
        [JsonProperty("signature")]
        public string Signature { get; set; }
        
        [JsonProperty("message")]
        public string Message { get; set; }
        
        [JsonProperty("callbackUrl")]
        public string CallbackUrl { get; set; }
    }

    // Plurality wallet verification response
    public class PluralityWalletVerificationResponse
    {
        [JsonProperty("verificationId")]
        public string VerificationId { get; set; }
        
        [JsonProperty("status")]
        public string Status { get; set; }
        
        [JsonProperty("redirectUrl")]
        public string RedirectUrl { get; set; }
    }

    // Plurality verification callback
    public class PluralityVerificationCallback
    {
        [JsonProperty("verificationId")]
        public string VerificationId { get; set; }
        
        [JsonProperty("walletAddress")]
        public string WalletAddress { get; set; }
        
        [JsonProperty("status")]
        public string Status { get; set; }
        
        [JsonProperty("timestamp")]
        public long TimestampUnix { get; set; }
        
        [JsonProperty("metadata")]
        public Dictionary<string, string> Metadata { get; set; }
    }

    // Plurality cross-chain address linking
    public class CrossChainAddressLink
    {
        [JsonProperty("primaryWalletAddress")]
        public string PrimaryWalletAddress { get; set; }
        
        [JsonProperty("primaryChainId")]
        public string PrimaryChainId { get; set; }
        
        [JsonProperty("linkedWalletAddress")]
        public string LinkedWalletAddress { get; set; }
        
        [JsonProperty("linkedChainId")]
        public string LinkedChainId { get; set; }
        
        [JsonProperty("linkId")]
        public string LinkId { get; set; }
        
        [JsonProperty("status")]
        public string Status { get; set; }
        
        [JsonProperty("createdAt")]
        public DateTime CreatedAt { get; set; }
    }
}

