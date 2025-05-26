using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using VeritasVault.Plurality.Models;

namespace VeritasVault.Plurality.Services
{
    /// <summary>
    /// Service for interacting with Plurality API
    /// </summary>
    public class PluralityService
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger _logger;
        private readonly PluralityConfig _config;

        public PluralityService(HttpClient httpClient, ILogger logger, PluralityConfig config)
        {
            _httpClient = httpClient;
            _logger = logger;
            _config = config;
            
            // Configure HTTP client
            _httpClient.BaseAddress = new Uri(_config.ApiUrl);
            _httpClient.DefaultRequestHeaders.Accept.Clear();
            _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            _httpClient.DefaultRequestHeaders.Add("X-API-Key", _config.ApiKey);
        }

        /// <summary>
        /// Initiates wallet verification through Plurality
        /// </summary>
        public async Task<PluralityApiResponse<PluralityWalletVerificationResponse>> InitiateWalletVerification(PluralityWalletVerificationRequest request)
        {
            try
            {
                _logger.LogInformation($"Initiating wallet verification for address: {request.WalletAddress}");
                
                var content = new StringContent(JsonConvert.SerializeObject(request), Encoding.UTF8, "application/json");
                var response = await _httpClient.PostAsync("/api/v1/identity/verify-wallet", content);
                
                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    var result = JsonConvert.DeserializeObject<PluralityApiResponse<PluralityWalletVerificationResponse>>(responseContent);
                    
                    _logger.LogInformation($"Wallet verification initiated successfully. VerificationId: {result.Data.VerificationId}");
                    return result;
                }
                else
                {
                    _logger.LogError($"Failed to initiate wallet verification. Status: {response.StatusCode}");
                    return new PluralityApiResponse<PluralityWalletVerificationResponse>
                    {
                        Success = false,
                        Error = $"API request failed with status code: {response.StatusCode}",
                        Message = "Failed to initiate wallet verification"
                    };
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Exception occurred while initiating wallet verification");
                return new PluralityApiResponse<PluralityWalletVerificationResponse>
                {
                    Success = false,
                    Error = ex.Message,
                    Message = "Exception occurred while initiating wallet verification"
                };
            }
        }

        /// <summary>
        /// Checks the status of a wallet verification
        /// </summary>
        public async Task<PluralityApiResponse<IdentityVerification>> CheckVerificationStatus(string verificationId)
        {
            try
            {
                _logger.LogInformation($"Checking verification status for ID: {verificationId}");
                
                var response = await _httpClient.GetAsync($"/api/v1/identity/verification-status/{verificationId}");
                
                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    var result = JsonConvert.DeserializeObject<PluralityApiResponse<IdentityVerification>>(responseContent);
                    
                    _logger.LogInformation($"Verification status check successful. Status: {result.Data.Status}");
                    return result;
                }
                else
                {
                    _logger.LogError($"Failed to check verification status. Status: {response.StatusCode}");
                    return new PluralityApiResponse<IdentityVerification>
                    {
                        Success = false,
                        Error = $"API request failed with status code: {response.StatusCode}",
                        Message = "Failed to check verification status"
                    };
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Exception occurred while checking verification status");
                return new PluralityApiResponse<IdentityVerification>
                {
                    Success = false,
                    Error = ex.Message,
                    Message = "Exception occurred while checking verification status"
                };
            }
        }

        /// <summary>
        /// Gets all verified addresses for a user
        /// </summary>
        public async Task<PluralityApiResponse<CrossChainAddressLink[]>> GetVerifiedAddresses(string walletAddress, string chainId)
        {
            try
            {
                _logger.LogInformation($"Getting verified addresses for wallet: {walletAddress} on chain: {chainId}");
                
                var response = await _httpClient.GetAsync($"/api/v1/identity/verified-addresses?walletAddress={walletAddress}&chainId={chainId}");
                
                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    var result = JsonConvert.DeserializeObject<PluralityApiResponse<CrossChainAddressLink[]>>(responseContent);
                    
                    _logger.LogInformation($"Retrieved {result.Data.Length} verified addresses for wallet: {walletAddress}");
                    return result;
                }
                else
                {
                    _logger.LogError($"Failed to get verified addresses. Status: {response.StatusCode}");
                    return new PluralityApiResponse<CrossChainAddressLink[]>
                    {
                        Success = false,
                        Error = $"API request failed with status code: {response.StatusCode}",
                        Message = "Failed to get verified addresses"
                    };
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Exception occurred while getting verified addresses");
                return new PluralityApiResponse<CrossChainAddressLink[]>
                {
                    Success = false,
                    Error = ex.Message,
                    Message = "Exception occurred while getting verified addresses"
                };
            }
        }

        /// <summary>
        /// Links a new wallet address to an existing verified wallet
        /// </summary>
        public async Task<PluralityApiResponse<CrossChainAddressLink>> LinkWalletAddress(string primaryWalletAddress, string primaryChainId, string linkedWalletAddress, string linkedChainId, string signature, string message)
        {
            try
            {
                _logger.LogInformation($"Linking wallet address: {linkedWalletAddress} to primary wallet: {primaryWalletAddress}");
                
                var request = new
                {
                    primaryWalletAddress,
                    primaryChainId,
                    linkedWalletAddress,
                    linkedChainId,
                    signature,
                    message
                };
                
                var content = new StringContent(JsonConvert.SerializeObject(request), Encoding.UTF8, "application/json");
                var response = await _httpClient.PostAsync("/api/v1/identity/link-address", content);
                
                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    var result = JsonConvert.DeserializeObject<PluralityApiResponse<CrossChainAddressLink>>(responseContent);
                    
                    _logger.LogInformation($"Wallet address linked successfully. LinkId: {result.Data.LinkId}");
                    return result;
                }
                else
                {
                    _logger.LogError($"Failed to link wallet address. Status: {response.StatusCode}");
                    return new PluralityApiResponse<CrossChainAddressLink>
                    {
                        Success = false,
                        Error = $"API request failed with status code: {response.StatusCode}",
                        Message = "Failed to link wallet address"
                    };
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Exception occurred while linking wallet address");
                return new PluralityApiResponse<CrossChainAddressLink>
                {
                    Success = false,
                    Error = ex.Message,
                    Message = "Exception occurred while linking wallet address"
                };
            }
        }
    }
}

