using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Newtonsoft.Json;
using VeritasVault.Plurality.Models;

namespace VeritasVault.Plurality.Tests
{
    [TestClass]
    public class PerformanceTests
    {
        private readonly HttpClient _httpClient;
        private readonly string _baseUrl;
        private readonly string _testWalletAddress;
        private readonly string _testSignature;
        private readonly string _testMessage;
        private readonly string _testChainId;
        private readonly int _numberOfIterations = 5;

        public PerformanceTests()
        {
            _httpClient = new HttpClient();
            _baseUrl = Environment.GetEnvironmentVariable("TEST_FUNCTION_BASE_URL") ?? "http://localhost:7071";
            _testWalletAddress = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e";
            _testSignature = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1b";
            _testMessage = "Connect wallet 0x742d35Cc6634C0532925a3b844Bc454e4438f44e to VeritasVault.ai\nNonce: 123456789\nTimestamp: 1621234567";
            _testChainId = "1"; // Ethereum Mainnet
        }

        [TestMethod]
        public async Task TC_6_1_ConnectionTime_Measurement()
        {
            // Arrange
            var request = new WalletConnectionRequest
            {
                WalletAddress = _testWalletAddress,
                WalletType = "MetaMask",
                ChainId = _testChainId,
                Signature = _testSignature,
                Message = _testMessage,
                TimestampUnix = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
            };

            var content = new StringContent(JsonConvert.SerializeObject(request), Encoding.UTF8, "application/json");
            var times = new List<long>();
            var stopwatch = new Stopwatch();

            // Act
            for (int i = 0; i < _numberOfIterations; i++)
            {
                stopwatch.Restart();
                var response = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/connect", content);
                stopwatch.Stop();
                
                times.Add(stopwatch.ElapsedMilliseconds);
                
                Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to connect wallet in iteration {i+1}");
                
                // Wait a bit between requests
                await Task.Delay(500);
            }

            // Calculate statistics
            var averageTime = times.Average();
            var minTime = times.Min();
            var maxTime = times.Max();

            // Assert
            Assert.IsTrue(averageTime < 5000, $"Average connection time ({averageTime}ms) exceeds the 5000ms threshold");
            
            Console.WriteLine($"Connection Time Performance Test Results:");
            Console.WriteLine($"Number of iterations: {_numberOfIterations}");
            Console.WriteLine($"Average time: {averageTime}ms");
            Console.WriteLine($"Minimum time: {minTime}ms");
            Console.WriteLine($"Maximum time: {maxTime}ms");
            Console.WriteLine($"All times (ms): {string.Join(", ", times)}");
        }

        [TestMethod]
        public async Task TC_6_2_TransactionProcessingTime_Measurement()
        {
            // Arrange
            var request = new WalletTransactionRequest
            {
                ConnectionId = "test-connection-id",
                WalletAddress = _testWalletAddress,
                TransactionType = "Deposit",
                TransactionData = JsonConvert.SerializeObject(new
                {
                    tokenAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC
                    amount = "100.0",
                    recipient = "0x1234567890123456789012345678901234567890" // Vault address
                }),
                ChainId = _testChainId,
                TimestampUnix = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
            };

            var content = new StringContent(JsonConvert.SerializeObject(request), Encoding.UTF8, "application/json");
            var times = new List<long>();
            var stopwatch = new Stopwatch();

            // Act
            for (int i = 0; i < _numberOfIterations; i++)
            {
                stopwatch.Restart();
                var response = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/transaction", content);
                stopwatch.Stop();
                
                times.Add(stopwatch.ElapsedMilliseconds);
                
                Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to process transaction in iteration {i+1}");
                
                // Wait a bit between requests
                await Task.Delay(500);
            }

            // Calculate statistics
            var averageTime = times.Average();
            var minTime = times.Min();
            var maxTime = times.Max();

            // Assert
            Assert.IsTrue(averageTime < 3000, $"Average transaction processing time ({averageTime}ms) exceeds the 3000ms threshold");
            
            Console.WriteLine($"Transaction Processing Time Performance Test Results:");
            Console.WriteLine($"Number of iterations: {_numberOfIterations}");
            Console.WriteLine($"Average time: {averageTime}ms");
            Console.WriteLine($"Minimum time: {minTime}ms");
            Console.WriteLine($"Maximum time: {maxTime}ms");
            Console.WriteLine($"All times (ms): {string.Join(", ", times)}");
        }

        [TestMethod]
        public async Task TC_6_3_WalletStatusTime_Measurement()
        {
            // Arrange
            var times = new List<long>();
            var stopwatch = new Stopwatch();

            // Act
            for (int i = 0; i < _numberOfIterations; i++)
            {
                stopwatch.Restart();
                var response = await _httpClient.GetAsync($"{_baseUrl}/api/wallet/status?connectionId=test-connection-id&walletAddress={_testWalletAddress}");
                stopwatch.Stop();
                
                times.Add(stopwatch.ElapsedMilliseconds);
                
                Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to get wallet status in iteration {i+1}");
                
                // Wait a bit between requests
                await Task.Delay(500);
            }

            // Calculate statistics
            var averageTime = times.Average();
            var minTime = times.Min();
            var maxTime = times.Max();

            // Assert
            Assert.IsTrue(averageTime < 2000, $"Average wallet status time ({averageTime}ms) exceeds the 2000ms threshold");
            
            Console.WriteLine($"Wallet Status Time Performance Test Results:");
            Console.WriteLine($"Number of iterations: {_numberOfIterations}");
            Console.WriteLine($"Average time: {averageTime}ms");
            Console.WriteLine($"Minimum time: {minTime}ms");
            Console.WriteLine($"Maximum time: {maxTime}ms");
            Console.WriteLine($"All times (ms): {string.Join(", ", times)}");
        }

        [TestMethod]
        public async Task TC_6_4_WalletBalanceTime_Measurement()
        {
            // Arrange
            var times = new List<long>();
            var stopwatch = new Stopwatch();

            // Act
            for (int i = 0; i < _numberOfIterations; i++)
            {
                stopwatch.Restart();
                var response = await _httpClient.GetAsync($"{_baseUrl}/api/wallet/balance?walletAddress={_testWalletAddress}&chainId={_testChainId}");
                stopwatch.Stop();
                
                times.Add(stopwatch.ElapsedMilliseconds);
                
                Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to get wallet balance in iteration {i+1}");
                
                // Wait a bit between requests
                await Task.Delay(500);
            }

            // Calculate statistics
            var averageTime = times.Average();
            var minTime = times.Min();
            var maxTime = times.Max();

            // Assert
            Assert.IsTrue(averageTime < 2000, $"Average wallet balance time ({averageTime}ms) exceeds the 2000ms threshold");
            
            Console.WriteLine($"Wallet Balance Time Performance Test Results:");
            Console.WriteLine($"Number of iterations: {_numberOfIterations}");
            Console.WriteLine($"Average time: {averageTime}ms");
            Console.WriteLine($"Minimum time: {minTime}ms");
            Console.WriteLine($"Maximum time: {maxTime}ms");
            Console.WriteLine($"All times (ms): {string.Join(", ", times)}");
        }
    }
}

