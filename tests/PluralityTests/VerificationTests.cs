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
    public class VerificationTests
    {
        private readonly HttpClient _httpClient;
        private readonly string _baseUrl;
        private readonly string _testWalletAddress;
        private readonly string _testConnectionId;
        private readonly string _testChainId;

        public VerificationTests()
        {
            _httpClient = new HttpClient();
            _baseUrl = Environment.GetEnvironmentVariable("TEST_FUNCTION_BASE_URL") ?? "http://localhost:7071";
            _testWalletAddress = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e";
            _testConnectionId = "test-connection-id";
            _testChainId = "1"; // Ethereum Mainnet
        }

        [TestMethod]
        public async Task TC_2_1_GetWalletStatus_Success()
        {
            // Act
            var response = await _httpClient.GetAsync($"{_baseUrl}/api/wallet/status?connectionId={_testConnectionId}&walletAddress={_testWalletAddress}");
            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonConvert.DeserializeObject<WalletStatus>(responseContent);

            // Assert
            Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to get wallet status: {responseContent}");
            Assert.IsNotNull(result, "Response should not be null");
            Assert.AreEqual(_testConnectionId, result.ConnectionId, "ConnectionId should match the request");
            Assert.AreEqual(_testWalletAddress, result.WalletAddress, "WalletAddress should match the request");
            Assert.IsNotNull(result.VerificationStatus, "VerificationStatus should not be null");
            
            Console.WriteLine($"Successfully retrieved wallet status for: {result.WalletAddress}");
            Console.WriteLine($"ConnectionId: {result.ConnectionId}");
            Console.WriteLine($"WalletType: {result.WalletType}");
            Console.WriteLine($"ChainId: {result.ChainId}");
            Console.WriteLine($"IsConnected: {result.IsConnected}");
            Console.WriteLine($"VerificationStatus: {result.VerificationStatus}");
            Console.WriteLine($"LastActivity: {result.LastActivity}");
        }

        [TestMethod]
        public async Task TC_2_2_VerificationCallback_Success()
        {
            // Arrange
            var callback = new PluralityVerificationCallback
            {
                VerificationId = _testConnectionId,
                WalletAddress = _testWalletAddress,
                Status = "Verified",
                TimestampUnix = DateTimeOffset.UtcNow.ToUnixTimeSeconds(),
                Metadata = new System.Collections.Generic.Dictionary<string, string>
                {
                    { "level", "standard" },
                    { "provider", "Plurality" }
                }
            };

            var content = new StringContent(JsonConvert.SerializeObject(callback), Encoding.UTF8, "application/json");

            // Act
            var response = await _httpClient.PostAsync($"{_baseUrl}/api/verification-callback", content);

            // Assert
            Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to process verification callback: {await response.Content.ReadAsStringAsync()}");
            Assert.AreEqual(System.Net.HttpStatusCode.OK, response.StatusCode, "Status code should be 200 OK");
            
            Console.WriteLine($"Successfully processed verification callback for: {callback.WalletAddress}");
            Console.WriteLine($"VerificationId: {callback.VerificationId}");
            Console.WriteLine($"Status: {callback.Status}");
        }

        [TestMethod]
        public async Task TC_2_3_VerificationCallback_MissingParameters_BadRequest()
        {
            // Arrange - Missing required parameters
            var callback = new
            {
                WalletAddress = _testWalletAddress,
                Status = "Verified"
                // Missing VerificationId
            };

            var content = new StringContent(JsonConvert.SerializeObject(callback), Encoding.UTF8, "application/json");

            // Act
            var response = await _httpClient.PostAsync($"{_baseUrl}/api/verification-callback", content);
            var responseContent = await response.Content.ReadAsStringAsync();

            // Assert
            Assert.IsFalse(response.IsSuccessStatusCode, "Response should be a bad request");
            Assert.AreEqual(System.Net.HttpStatusCode.BadRequest, response.StatusCode, "Status code should be 400 Bad Request");
            Assert.IsTrue(responseContent.Contains("Invalid callback parameters"), "Error message should indicate invalid parameters");
            
            Console.WriteLine($"Bad request response as expected: {responseContent}");
        }

        [TestMethod]
        public async Task TC_7_1_SecurityTest_GetWalletStatus_MissingParameters_BadRequest()
        {
            // Act - Missing required parameters
            var response = await _httpClient.GetAsync($"{_baseUrl}/api/wallet/status?connectionId={_testConnectionId}");
            var responseContent = await response.Content.ReadAsStringAsync();

            // Assert
            Assert.IsFalse(response.IsSuccessStatusCode, "Response should be a bad request");
            Assert.AreEqual(System.Net.HttpStatusCode.BadRequest, response.StatusCode, "Status code should be 400 Bad Request");
            Assert.IsTrue(responseContent.Contains("Missing required parameters"), "Error message should indicate missing parameters");
            
            Console.WriteLine($"Bad request response as expected: {responseContent}");
        }

        [TestMethod]
        public async Task TC_7_2_SecurityTest_GetWalletBalance_MissingParameters_BadRequest()
        {
            // Act - Missing required parameters
            var response = await _httpClient.GetAsync($"{_baseUrl}/api/wallet/balance?walletAddress={_testWalletAddress}");
            var responseContent = await response.Content.ReadAsStringAsync();

            // Assert
            Assert.IsFalse(response.IsSuccessStatusCode, "Response should be a bad request");
            Assert.AreEqual(System.Net.HttpStatusCode.BadRequest, response.StatusCode, "Status code should be 400 Bad Request");
            Assert.IsTrue(responseContent.Contains("Missing required parameters"), "Error message should indicate missing parameters");
            
            Console.WriteLine($"Bad request response as expected: {responseContent}");
        }
    }
}

