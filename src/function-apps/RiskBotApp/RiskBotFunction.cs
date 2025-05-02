using System;
using System.Threading.Tasks;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.EventGrid;
using Microsoft.Extensions.Logging;
using Azure.Messaging.EventGrid;
using Newtonsoft.Json;
using StackExchange.Redis;
using System.Text.Json;
using VeritasVault.RiskBotApp.Models;

namespace VeritasVault.RiskBotApp
{
    public class RiskBotFunction
    {
        private readonly ILogger<RiskBotFunction> _logger;
        private readonly RiskApiClient _riskApiClient;
        private readonly ConnectionMultiplexer _redis;
        
        public RiskBotFunction(
            ILogger<RiskBotFunction> logger,
            RiskApiClient riskApiClient,
            ConnectionMultiplexer redis)
        {
            _logger = logger;
            _riskApiClient = riskApiClient;
            _redis = redis;
        }

        [FunctionName("ProcessBlockchainEvent")]
        public async Task Run(
            [EventGridTrigger] EventGridEvent eventGridEvent)
        {
            try
            {
                _logger.LogInformation($"Processing event: {eventGridEvent.EventType} - {eventGridEvent.Id}");
                
                // 1. Deserialize and validate the event payload
                var blockchainEvent = JsonConvert.DeserializeObject<BlockchainEvent>(eventGridEvent.Data.ToString());
                
                if (blockchainEvent == null)
                {
                    _logger.LogError($"Failed to deserialize event data: {eventGridEvent.Data}");
                    throw new Exception("Invalid event payload format");
                }
                
                // 2. Prepare data for ML model
                var riskPredictionRequest = Helpers.MapToRiskPredictionRequest(blockchainEvent);
                
                // 3. Call ML service for risk prediction
                var riskPrediction = await _riskApiClient.GetRiskPredictionAsync(riskPredictionRequest);
                
                if (riskPrediction == null)
                {
                    _logger.LogError("Failed to get risk prediction from ML service");
                    throw new Exception("ML service returned null response");
                }
                
                _logger.LogInformation($"Received prediction: LTV={riskPrediction.Ltv}, TVL={riskPrediction.Tvl}");
                
                // 4. Store results in Redis for downstream consumers
                var db = _redis.GetDatabase();
                
                // Create metrics object for storage
                var vaultMetrics = Helpers.MapToVaultMetrics(riskPrediction, eventGridEvent.Id);
                string metricsJson = JsonSerializer.Serialize(vaultMetrics);
                
                // Store by vault ID for quick lookup
                string vaultKey = Helpers.GenerateVaultMetricsKey(blockchainEvent.VaultId, blockchainEvent.Network);
                await db.StringSetAsync(vaultKey, metricsJson);
                
                // Also add to time-series data for historical tracking
                string timeSeriesKey = Helpers.GenerateVaultHistoryKey(blockchainEvent.VaultId, blockchainEvent.Network);
                await db.SortedSetAddAsync(
                    timeSeriesKey, 
                    metricsJson, 
                    DateTimeOffset.UtcNow.ToUnixTimeMilliseconds());
                
                _logger.LogInformation($"Successfully processed event {eventGridEvent.Id}");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error processing event {eventGridEvent.Id}: {ex.Message}");
                throw; // Let EventGrid retry based on retry policy
            }
        }
    }
}