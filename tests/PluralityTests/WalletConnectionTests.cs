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
    public class WalletConnectionTests
    {
        private readonly HttpClient _httpClient;
        private readonly string _baseUrl;
        private readonly string _testWalletAddress;
        private readonly string _testSignature;
        private readonly string _testMessage;
        private readonly string _testChainId;

        public WalletConnectionTests()
        {
            _httpClient = new HttpClient();
            _baseUrl = Environment.GetEnvironmentVariable("TEST_FUNCTION_BASE_URL") ?? "http://localhost:7071";
            _testWalletAddress = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e";
            _testSignature = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1b";
            _testMessage = "Connect wallet 0x742d35Cc6634C0532925a3b844Bc454e4438f44e to VeritasVault.ai\nNonce: 123456789\nTimestamp: 1621234567";
            _testChainId = "1"; // Ethereum Mainnet
        }

        [TestMethod]
        public async Task TC_1_1_ConnectWallet_ValidSignature_Success()
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

            // Act
            var response = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/connect", content);
            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonConvert.DeserializeObject<WalletConnectionResponse>(responseContent);

            // Assert
            Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to connect wallet: {responseContent}");
            Assert.IsNotNull(result, "Response should not be null");
            Assert.AreEqual("Connected", result.Status, "Wallet should be connected");
            Assert.IsNotNull(result.ConnectionId, "ConnectionId should not be null");
            Assert.AreEqual(_testWalletAddress, result.WalletAddress, "WalletAddress should match the request");
            
            Console.WriteLine($"Successfully connected wallet: {result.WalletAddress}");
            Console.WriteLine($"ConnectionId: {result.ConnectionId}");
            Console.WriteLine($"Status: {result.Status}");
            Console.WriteLine($"Message: {result.Message}");
        }

        [TestMethod]
        public async Task TC_1_2_ConnectWallet_InvalidSignature_Failure()
        {
            // Arrange
            var request = new WalletConnectionRequest
            {
                WalletAddress = _testWalletAddress,
                WalletType = "MetaMask",
                ChainId = _testChainId,
                Signature = "0xInvalidSignature",
                Message = _testMessage,
                TimestampUnix = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
            };

            var content = new StringContent(JsonConvert.SerializeObject(request), Encoding.UTF8, "application/json");

            // Act
            var response = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/connect", content);
            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonConvert.DeserializeObject<WalletConnectionResponse>(responseContent);

            // Assert
            Assert.IsTrue(response.IsSuccessStatusCode, "Response should be successful even for invalid signature");
            Assert.IsNotNull(result, "Response should not be null");
            Assert.AreEqual("Failed", result.Status, "Wallet connection should fail");
            Assert.IsTrue(result.Message.Contains("Invalid signature"), "Error message should indicate invalid signature");
            
            Console.WriteLine($"Failed to connect wallet as expected: {result.Message}");
        }

        [TestMethod]
        public async Task TC_1_3_DisconnectWallet_Success()
        {
            // Arrange - First connect a wallet
            var connectRequest = new WalletConnectionRequest
            {
                WalletAddress = _testWalletAddress,
                WalletType = "MetaMask",
                ChainId = _testChainId,
                Signature = _testSignature,
                Message = _testMessage,
                TimestampUnix = DateTimeOffset.UtcNow.ToUnixTimeSeconds()
            };

            var connectContent = new StringContent(JsonConvert.SerializeObject(connectRequest), Encoding.UTF8, "application/json");
            var connectResponse = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/connect", connectContent);
            var connectResponseContent = await connectResponse.Content.ReadAsStringAsync();
            var connectResult = JsonConvert.DeserializeObject<WalletConnectionResponse>(connectResponseContent);

            Assert.IsTrue(connectResponse.IsSuccessStatusCode, "Failed to connect wallet for disconnect test");
            
            // Now disconnect the wallet
            var disconnectRequest = new
            {
                connectionId = connectResult.ConnectionId,
                walletAddress = _testWalletAddress
            };

            var disconnectContent = new StringContent(JsonConvert.SerializeObject(disconnectRequest), Encoding.UTF8, "application/json");

            // Act
            var response = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/disconnect", disconnectContent);
            var responseContent = await response.Content.ReadAsStringAsync();
            var result = JsonConvert.DeserializeObject<WalletConnectionResponse>(responseContent);

            // Assert
            Assert.IsTrue(response.IsSuccessStatusCode, $"Failed to disconnect wallet: {responseContent}");
            Assert.IsNotNull(result, "Response should not be null");
            Assert.AreEqual("Disconnected", result.Status, "Wallet should be disconnected");
            Assert.AreEqual(_testWalletAddress, result.WalletAddress, "WalletAddress should match the request");
            
            Console.WriteLine($"Successfully disconnected wallet: {result.WalletAddress}");
            Console.WriteLine($"ConnectionId: {result.ConnectionId}");
            Console.WriteLine($"Status: {result.Status}");
            Console.WriteLine($"Message: {result.Message}");
        }

        [TestMethod]
        public async Task TC_5_1_ConnectWallet_MissingParameters_BadRequest()
        {
            // Arrange - Missing required parameters
            var request = new
            {
                WalletType = "MetaMask",
                ChainId = _testChainId
                // Missing WalletAddress, Signature, and Message
            };

            var content = new StringContent(JsonConvert.SerializeObject(request), Encoding.UTF8, "application/json");

            // Act
            var response = await _httpClient.PostAsync($"{_baseUrl}/api/wallet/connect", content);
            var responseContent = await response.Content.ReadAsStringAsync();

            // Assert
            Assert.IsFalse(response.IsSuccessStatusCode, "Response should be a bad request");
            Assert.AreEqual(System.Net.HttpStatusCode.BadRequest, response.StatusCode, "Status code should be 400 Bad Request");
            Assert.IsTrue(responseContent.Contains("Invalid request parameters"), "Error message should indicate invalid parameters");
            
            Console.WriteLine($"Bad request response as expected: {responseContent}");
        }
    }
}

