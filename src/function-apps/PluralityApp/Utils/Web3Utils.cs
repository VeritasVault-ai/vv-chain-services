using System;
using System.Numerics;
using System.Text;
using Nethereum.Signer;
using Nethereum.Util;

namespace VeritasVault.Plurality.Utils
{
    /// <summary>
    /// Utilities for Web3 operations
    /// </summary>
    public static class Web3Utils
    {
        /// <summary>
        /// Verifies an Ethereum signature
        /// </summary>
        /// <param name="message">The original message that was signed</param>
        /// <param name="signature">The signature to verify</param>
        /// <param name="address">The Ethereum address that supposedly signed the message</param>
        /// <returns>True if the signature is valid, false otherwise</returns>
        public static bool VerifySignature(string message, string signature, string address)
        {
            try
            {
                // Ensure the signature has the correct format
                if (!signature.StartsWith("0x"))
                {
                    signature = "0x" + signature;
                }
                
                // Ensure the address has the correct format
                if (!address.StartsWith("0x"))
                {
                    address = "0x" + address;
                }
                
                // Create the Ethereum message prefix
                var prefix = $"\x19Ethereum Signed Message:\n{message.Length}";
                var prefixedMessage = prefix + message;
                
                // Hash the prefixed message
                var hash = new Sha3Keccack().CalculateHash(Encoding.UTF8.GetBytes(prefixedMessage));
                
                // Recover the signer address from the signature
                var signer = new EthereumMessageSigner();
                var recoveredAddress = signer.EncodeUTF8AndEcRecover(message, signature);
                
                // Compare the recovered address with the provided address
                return string.Equals(recoveredAddress, address, StringComparison.OrdinalIgnoreCase);
            }
            catch (Exception)
            {
                // If any exception occurs during verification, consider the signature invalid
                return false;
            }
        }

        /// <summary>
        /// Generates a nonce for signing
        /// </summary>
        /// <returns>A random nonce as a string</returns>
        public static string GenerateNonce()
        {
            return Guid.NewGuid().ToString();
        }

        /// <summary>
        /// Creates a standard message for wallet connection
        /// </summary>
        /// <param name="walletAddress">The wallet address</param>
        /// <param name="nonce">A random nonce</param>
        /// <param name="timestamp">Unix timestamp</param>
        /// <returns>A formatted message for signing</returns>
        public static string CreateConnectionMessage(string walletAddress, string nonce, long timestamp)
        {
            return $"Connect wallet {walletAddress} to VeritasVault.ai\nNonce: {nonce}\nTimestamp: {timestamp}";
        }

        /// <summary>
        /// Converts a hex string to a byte array
        /// </summary>
        /// <param name="hex">The hex string to convert</param>
        /// <returns>A byte array</returns>
        public static byte[] HexToByteArray(string hex)
        {
            if (hex.StartsWith("0x"))
            {
                hex = hex.Substring(2);
            }
            
            byte[] bytes = new byte[hex.Length / 2];
            for (int i = 0; i < bytes.Length; i++)
            {
                bytes[i] = Convert.ToByte(hex.Substring(i * 2, 2), 16);
            }
            
            return bytes;
        }

        /// <summary>
        /// Converts a byte array to a hex string
        /// </summary>
        /// <param name="bytes">The byte array to convert</param>
        /// <returns>A hex string</returns>
        public static string ByteArrayToHex(byte[] bytes)
        {
            StringBuilder hex = new StringBuilder(bytes.Length * 2);
            foreach (byte b in bytes)
            {
                hex.AppendFormat("{0:x2}", b);
            }
            
            return "0x" + hex.ToString();
        }
    }
}

