# Plurality Function App

## Overview

The Plurality Function App provides backend services for wallet integration via Plurality, with a focus on MetaMask integration. This component serves as the bridge between the VeritasVault.ai platform and Plurality services, enabling secure wallet connections, identity verification, and transaction processing.

## Features

- **MetaMask Integration**: Connect MetaMask wallets securely through Plurality
- **Identity Verification**: Verify user identity using Plurality's verification services
- **Cross-Chain Address Linking**: Link multiple wallet addresses across different chains
- **Transaction Processing**: Process wallet transactions securely
- **Wallet Status & Balance**: Retrieve wallet connection status and balances

## Architecture

The Plurality Function App consists of the following components:

- **WalletFunctions.cs**: Azure Functions for handling wallet-related HTTP requests
- **Services/MetaMaskService.cs**: Service for MetaMask wallet integration
- **Services/PluralityService.cs**: Service for interacting with Plurality API
- **Models/WalletModels.cs**: Data models for wallet integration
- **Models/PluralityModels.cs**: Data models for Plurality integration
- **Utils/Web3Utils.cs**: Utilities for Web3 operations like signature verification

## API Endpoints

### Wallet Connection

- **POST /api/wallet/connect**: Connect a MetaMask wallet
  - Request: `WalletConnectionRequest`
  - Response: `WalletConnectionResponse`

### Wallet Disconnection

- **POST /api/wallet/disconnect**: Disconnect a wallet
  - Request: `{ connectionId, walletAddress }`
  - Response: `WalletConnectionResponse`

### Wallet Status

- **GET /api/wallet/status**: Get wallet connection status
  - Query Parameters: `connectionId`, `walletAddress`
  - Response: `WalletStatus`

### Wallet Balance

- **GET /api/wallet/balance**: Get wallet balance
  - Query Parameters: `walletAddress`, `chainId`
  - Response: `WalletBalance`

### Transaction Processing

- **POST /api/wallet/transaction**: Process a wallet transaction
  - Request: `WalletTransactionRequest`
  - Response: `WalletTransactionResponse`

### Verification Callback

- **POST /api/verification-callback**: Handle verification callbacks from Plurality
  - Request: `PluralityVerificationCallback`
  - Response: HTTP 200 OK

## Configuration

The Plurality Function App requires the following configuration settings:

```json
{
  "PLURALITY_API_URL": "https://api.plurality.network",
  "PLURALITY_API_KEY": "your-api-key",
  "PLURALITY_API_SECRET": "your-api-secret",
  "PLURALITY_WEBHOOK_URL": "https://your-webhook-url",
  "PLURALITY_VERIFICATION_LEVEL": "standard",
  "FUNCTION_BASE_URL": "https://your-function-app-url"
}
```

## Deployment

To deploy the Plurality Function App:

```bash
cd src/function-apps/PluralityApp
func azure functionapp publish <plurality-function-app-name>
```

## Dependencies

- **Nethereum**: For Ethereum signature verification and Web3 operations
- **Newtonsoft.Json**: For JSON serialization/deserialization
- **Microsoft.Azure.WebJobs**: For Azure Functions runtime
- **Microsoft.Extensions.Logging**: For logging

## Security Considerations

- All API endpoints use Azure Function authorization
- Wallet signatures are verified using cryptographic methods
- Plurality API calls use secure authentication
- No private keys are ever stored or transmitted
- All sensitive configuration is stored in Azure Key Vault

