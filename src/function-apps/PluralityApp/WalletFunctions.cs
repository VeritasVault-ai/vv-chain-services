using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using VeritasVault.Plurality.Models;
using VeritasVault.Plurality.Services;
using System.Net.Http;

namespace VeritasVault.Plurality.Functions
{
    /// <summary>
    /// Azure Functions for wallet integration
    /// </summary>
    public class WalletFunctions
    {
        private readonly MetaMaskService _metaMaskService;
        private readonly PluralityService _pluralityService;
        private readonly ILogger<WalletFunctions> _logger;
        private readonly HttpClient _httpClient;

        public WalletFunctions(ILogger<WalletFunctions> logger)
        {
            _logger = logger;
            _httpClient = new HttpClient();
            
            // Load configuration
            var pluralityConfig = new PluralityConfig
            {
                ApiUrl = Environment.GetEnvironmentVariable("PLURALITY_API_URL"),
                ApiKey = Environment.GetEnvironmentVariable("PLURALITY_API_KEY"),
                ApiSecret = Environment.GetEnvironmentVariable("PLURALITY_API_SECRET"),
                WebhookUrl = Environment.GetEnvironmentVariable("PLURALITY_WEBHOOK_URL"),
                VerificationLevel = Environment.GetEnvironmentVariable("PLURALITY_VERIFICATION_LEVEL")
            };
            
            // Initialize services
            _pluralityService = new PluralityService(_httpClient, _logger, pluralityConfig);
            _metaMaskService = new MetaMaskService(_pluralityService, _logger, _httpClient);
        }

        /// <summary>
        /// Connects a wallet
        /// </summary>
        [FunctionName("ConnectWallet")]
        public async Task<IActionResult> ConnectWallet(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = "wallet/connect")] HttpRequest req)
        {
            _logger.LogInformation("Processing wallet connection request");

            try
            {
                // Read request body
                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                var request = JsonConvert.DeserializeObject<WalletConnectionRequest>(requestBody);
                
                // Validate request
                if (request == null || string.IsNullOrEmpty(request.WalletAddress) || 
                    string.IsNullOrEmpty(request.Signature) || string.IsNullOrEmpty(request.Message))
                {
                    return new BadRequestObjectResult("Invalid request parameters");
                }
                
                // Process wallet connection
                var response = await _metaMaskService.ConnectWallet(request);
                
                return new OkObjectResult(response);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing wallet connection request");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }

        /// <summary>
        /// Disconnects a wallet
        /// </summary>
        [FunctionName("DisconnectWallet")]
        public async Task<IActionResult> DisconnectWallet(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = "wallet/disconnect")] HttpRequest req)
        {
            _logger.LogInformation("Processing wallet disconnection request");

            try
            {
                // Read request body
                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                var request = JsonConvert.DeserializeObject<dynamic>(requestBody);
                
                // Validate request
                if (request == null || string.IsNullOrEmpty((string)request.connectionId) || 
                    string.IsNullOrEmpty((string)request.walletAddress))
                {
                    return new BadRequestObjectResult("Invalid request parameters");
                }
                
                // Process wallet disconnection
                var response = await _metaMaskService.DisconnectWallet(
                    (string)request.connectionId, 
                    (string)request.walletAddress);
                
                return new OkObjectResult(response);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing wallet disconnection request");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }

        /// <summary>
        /// Gets wallet status
        /// </summary>
        [FunctionName("GetWalletStatus")]
        public async Task<IActionResult> GetWalletStatus(
            [HttpTrigger(AuthorizationLevel.Function, "get", Route = "wallet/status")] HttpRequest req)
        {
            _logger.LogInformation("Processing wallet status request");

            try
            {
                // Get query parameters
                string connectionId = req.Query["connectionId"];
                string walletAddress = req.Query["walletAddress"];
                
                // Validate parameters
                if (string.IsNullOrEmpty(connectionId) || string.IsNullOrEmpty(walletAddress))
                {
                    return new BadRequestObjectResult("Missing required parameters: connectionId, walletAddress");
                }
                
                // Get wallet status
                var status = await _metaMaskService.GetWalletStatus(connectionId, walletAddress);
                
                return new OkObjectResult(status);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing wallet status request");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }

        /// <summary>
        /// Gets wallet balance
        /// </summary>
        [FunctionName("GetWalletBalance")]
        public async Task<IActionResult> GetWalletBalance(
            [HttpTrigger(AuthorizationLevel.Function, "get", Route = "wallet/balance")] HttpRequest req)
        {
            _logger.LogInformation("Processing wallet balance request");

            try
            {
                // Get query parameters
                string walletAddress = req.Query["walletAddress"];
                string chainId = req.Query["chainId"];
                
                // Validate parameters
                if (string.IsNullOrEmpty(walletAddress) || string.IsNullOrEmpty(chainId))
                {
                    return new BadRequestObjectResult("Missing required parameters: walletAddress, chainId");
                }
                
                // Get wallet balance
                var balance = await _metaMaskService.GetWalletBalance(walletAddress, chainId);
                
                return new OkObjectResult(balance);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing wallet balance request");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }

        /// <summary>
        /// Processes a wallet transaction
        /// </summary>
        [FunctionName("ProcessTransaction")]
        public async Task<IActionResult> ProcessTransaction(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = "wallet/transaction")] HttpRequest req)
        {
            _logger.LogInformation("Processing wallet transaction request");

            try
            {
                // Read request body
                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                var request = JsonConvert.DeserializeObject<WalletTransactionRequest>(requestBody);
                
                // Validate request
                if (request == null || string.IsNullOrEmpty(request.ConnectionId) || 
                    string.IsNullOrEmpty(request.WalletAddress) || string.IsNullOrEmpty(request.TransactionType))
                {
                    return new BadRequestObjectResult("Invalid request parameters");
                }
                
                // Process transaction
                var response = await _metaMaskService.ProcessTransaction(request);
                
                return new OkObjectResult(response);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing wallet transaction request");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }

        /// <summary>
        /// Handles verification callbacks from Plurality
        /// </summary>
        [FunctionName("VerificationCallback")]
        public async Task<IActionResult> VerificationCallback(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = "verification-callback")] HttpRequest req)
        {
            _logger.LogInformation("Processing verification callback");

            try
            {
                // Read request body
                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                var callback = JsonConvert.DeserializeObject<PluralityVerificationCallback>(requestBody);
                
                // Validate callback
                if (callback == null || string.IsNullOrEmpty(callback.VerificationId) || 
                    string.IsNullOrEmpty(callback.WalletAddress))
                {
                    return new BadRequestObjectResult("Invalid callback parameters");
                }
                
                // Log the callback
                _logger.LogInformation($"Received verification callback for ID: {callback.VerificationId}, " +
                                      $"Wallet: {callback.WalletAddress}, Status: {callback.Status}");
                
                // In a real implementation, you would update your database with the verification status
                // and potentially trigger other actions based on the status
                
                return new OkResult();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing verification callback");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }
    }
}

