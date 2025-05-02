using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Polly;
using Polly.Retry;
using VeritasVault.RiskBotApp.Models;

namespace VeritasVault.RiskBotApp
{
    public class RiskApiClient
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<RiskApiClient> _logger;
        private readonly string _mlEndpoint;
        private readonly AsyncRetryPolicy _retryPolicy;

        public RiskApiClient(
            HttpClient httpClient,
            IConfiguration configuration,
            ILogger<RiskApiClient> logger)
        {
            _httpClient = httpClient;
            _logger = logger;
            _mlEndpoint = configuration["ML_ENDPOINT"];

            // Configure retry policy with exponential backoff
            _retryPolicy = Policy
                .Handle<HttpRequestException>()
                .Or<TaskCanceledException>()
                .WaitAndRetryAsync(
                    3, // Number of retries
                    attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)), // Exponential backoff
                    (ex, timeSpan, retryCount, context) =>
                    {
                        _logger.LogWarning($"Attempt {retryCount}: Retrying ML API call after {timeSpan.TotalSeconds}s due to: {ex.Message}");
                    });
        }

        public async Task<RiskPrediction> GetRiskPredictionAsync(RiskPredictionRequest request)
        {
            _logger.LogInformation($"Calling ML service for vault {request.VaultId}");

            return await _retryPolicy.ExecuteAsync(async () =>
            {
                var requestJson = JsonConvert.SerializeObject(request);
                var content = new StringContent(requestJson, Encoding.UTF8, "application/json");

                // Set timeout for the request
                using var cts = new System.Threading.CancellationTokenSource(TimeSpan.FromSeconds(10));
                
                var response = await _httpClient.PostAsync(_mlEndpoint, content, cts.Token);
                
                response.EnsureSuccessStatusCode();
                
                var responseBody = await response.Content.ReadAsStringAsync();
                var prediction = JsonConvert.DeserializeObject<RiskPrediction>(responseBody);
                
                if (prediction == null)
                {
                    throw new Exception("Failed to deserialize ML response");
                }
                
                return prediction;
            });
        }
    }
}