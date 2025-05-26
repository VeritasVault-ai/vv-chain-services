using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using Newtonsoft.Json;
using VeritasVault.Plurality.Models;

namespace VeritasVault.Plurality.Tests
{
    [TestClass]
    public class TransactionTests
    {
        private readonly HttpClient _httpClient;
        private readonly string _baseUrl;
        private readonly string _testWalletAddress;
        private readonly string _testConnectionId;
        private readonly string _testChainId;

        public TransactionTests()
        {
            _httpClient = new HttpClient();
            _baseUrl = Environment.GetEnvironmentVariable("TEST_FUNCTION_BASE_URL") ?? "http://localhost:7071";
            _testWalletAddress = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e";
            _testConnectionId = "test-connection-id";
            _testChainId = "1"; // Ethereum Mainnet
        }

        [TestMethod]
        public async Task TC_3_1_DepositTokens_Success()
        {
            // Arrange
            var request = new WalletTransactionRequest
            {
                ConnectionId = _testConnectionId,
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

            // Act
            var response = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/transaction", content);
            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonConvert.DeserializeObject<WalletTransactionResponse>(responseContent);

            // Assert
            Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to process deposit transaction: {responseContent}");
            Assert.IsNotNull(result, "Response should not be null");
            Assert.IsNotNull(result.TransactionId, "TransactionId should not be null");
            Assert.IsNotNull(result.TransactionHash, "TransactionHash should not be null");
            Assert.AreEqual("Pending", result.Status, "Transaction status should be Pending");
            
            Console.WriteLine($"Successfully initiated deposit transaction");
            Console.WriteLine($"TransactionId: {result.TransactionId}");
            Console.WriteLine($"TransactionHash: {result.TransactionHash}");
            Console.WriteLine($"Status: {result.Status}");
            Console.WriteLine($"Message: {result.Message}");
        }

        [TestMethod]
        public async Task TC_3_2_WithdrawAssets_Success()
        {
            // Arrange
            var request = new WalletTransactionRequest
            {
                ConnectionId = _testConnectionId,
                WalletAddress = _testWalletAddress,
                TransactionType = "Withdraw",
                TransactionData = JsonConvert.SerializeObject(new
                {
                    tokenAddress = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC
                    amount = "50.0",
                    recipient = _testWalletAddress
                }),
                ChainId = _testChainId,
                TimestampUnix = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
            };

            var content = new StringContent(JsonConvert.SerializeObject(request), Encoding.UTF8, "application/json");

            // Act
            var response = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/transaction", content);
            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonConvert.DeserializeObject<WalletTransactionResponse>(responseContent);

            // Assert
            Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to process withdrawal transaction: {responseContent}");
            Assert.IsNotNull(result, "Response should not be null");
            Assert.IsNotNull(result.TransactionId, "TransactionId should not be null");
            Assert.IsNotNull(result.TransactionHash, "TransactionHash should not be null");
            Assert.AreEqual("Pending", result.Status, "Transaction status should be Pending");
            
            Console.WriteLine($"Successfully initiated withdrawal transaction");
            Console.WriteLine($"TransactionId: {result.TransactionId}");
            Console.WriteLine($"TransactionHash: {result.TransactionHash}");
            Console.WriteLine($"Status: {result.Status}");
            Console.WriteLine($"Message: {result.Message}");
        }

        [TestMethod]
        public async Task TC_3_3_Transaction_MissingParameters_BadRequest()
        {
            // Arrange - Missing required parameters
            var request = new
            {
                WalletAddress = _testWalletAddress,
                TransactionType = "Deposit",
                // Missing ConnectionId and other required fields
            };

            var content = new StringContent(JsonConvert.SerializeObject(request), Encoding.UTF8, "application/json");

            // Act
            var response = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/transaction", content);
            var responseContent = await response.Content.ReadAsStringAsync();

            // Assert
            Assert.IsFalse(response.IsSuccessStatusCode, "Response should be a bad request");
            Assert.AreEqual(System.Net.HttpStatusCode.BadRequest, response.StatusCode, "Status code should be 400 Bad Request");
            Assert.IsTrue(responseContent.Contains("Invalid request parameters"), "Error message should indicate invalid parameters");
            
            Console.WriteLine($"Bad request response as expected: {responseContent}");
        }

        [TestMethod]
        public async Task TC_4_1_GovernanceVote_Success()
        {
            // Arrange
            var request = new WalletTransactionRequest
            {
                ConnectionId = _testConnectionId,
                WalletAddress = _testWalletAddress,
                TransactionType = "GovernanceVote",
                TransactionData = JsonConvert.SerializeObject(new
                {
                    proposalId = "1",
                    vote = "For", // For, Against, Abstain
                    reason = "I support this proposal"
                }),
                ChainId = _testChainId,
                TimestampUnix = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
            };

            var content = new StringContent(JsonConvert.SerializeObject(request), Encoding.UTF8, "application/json");

            // Act
            var response = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/transaction", content);
            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonConvert.DeserializeObject<WalletTransactionResponse>(responseContent);

            // Assert
            Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to process governance vote: {responseContent}");
            Assert.IsNotNull(result, "Response should not be null");
            Assert.IsNotNull(result.TransactionId, "TransactionId should not be null");
            Assert.IsNotNull(result.TransactionHash, "TransactionHash should not be null");
            Assert.AreEqual("Pending", result.Status, "Transaction status should be Pending");
            
            Console.WriteLine($"Successfully initiated governance vote");
            Console.WriteLine($"TransactionId: {result.TransactionId}");
            Console.WriteLine($"TransactionHash: {result.TransactionHash}");
            Console.WriteLine($"Status: {result.Status}");
            Console.WriteLine($"Message: {result.Message}");
        }

        [TestMethod]
        public async Task TC_GetWalletBalance_Success()
        {
            // Act
            var response = await _httpClient.GetAsync($"{_baseUrl}/api/wallet/balance?walletAddress={_testWalletAddress}&chainId={_testChainId}");
            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonConvert.DeserializeObject<WalletBalance>(responseContent);

            // Assert
            Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to get wallet balance: {responseContent}");
            Assert.IsNotNull(result, "Response should not be null");
            Assert.AreEqual(_testWalletAddress, result.WalletAddress, "WalletAddress should match the request");
            Assert.IsNotNull(result.Assets, "Assets should not be null");
            Assert.IsTrue(result.Assets.Count > 0, "Assets should not be empty");
            
            Console.WriteLine($"Successfully retrieved wallet balance for: {result.WalletAddress}");
            Console.WriteLine($"Number of assets: {result.Assets.Count}");
            foreach (var asset in result.Assets)
            {
                Console.WriteLine($"Asset: {asset.Symbol}, Amount: {asset.Amount}, Value: ${asset.ValueUsd}");
            }
        }
    }
}

