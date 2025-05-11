# EtherLink Integration Guide

## Overview

This document provides comprehensive guidance for integrating EtherLink within the VeritasVault.ai platform. EtherLink serves as a critical bridge between the Tezos and Ethereum ecosystems, enabling seamless cross-chain operations and expanding deployment options.

## Table of Contents

- [What is EtherLink?](#what-is-etherlink)
- [Architecture Overview](#architecture-overview)
- [Integration Components](#integration-components)
- [Getting Started](#getting-started)
- [SDK Usage](#sdk-usage)
- [Goldsky Subgraph Setup](#goldsky-subgraph-setup)
- [Cross-Chain Operations](#cross-chain-operations)
- [Security Considerations](#security-considerations)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)
- [Appendix: Technical Specifications](#appendix-technical-specifications)

## What is EtherLink?

EtherLink is an optimistic rollup solution that brings EVM compatibility to the Tezos blockchain. Launched in 2024, it enables developers to deploy Ethereum-compatible smart contracts on Tezos, benefiting from:

- **Lower Transaction Costs**: Average fees of $0.01-0.05 per transaction
- **High Throughput**: Processing capacity of 800-1,500 TPS
- **Cross-Ecosystem Compatibility**: Deploy once, operate across ecosystems
- **Security**: Leveraging Tezos' Proof-of-Stake consensus with optimistic rollup security

As of May 2025, EtherLink has established itself with approximately $1.1B in TVL, 85,000 daily active addresses, and 750,000 daily transactions.

## Architecture Overview

### EtherLink Technical Architecture

```
+---------------------+
|    Tezos L1 Chain   |
| (Settlement Layer)  |
+---------------------+
         ↑
         | Data Availability
         | & Settlement
         ↓
+---------------------+
|  EtherLink Rollup   |
| (Execution Layer)   |
+---------------------+
         ↑
         | EVM Compatibility
         | Layer
         ↓
+---------------------+
|  Ethereum-Compatible|
|  Smart Contracts    |
+---------------------+
```

### Integration with VeritasVault.ai

```
+---------------------+        +----------------------+
|  EtherLink Network  | <----> | Goldsky EtherLink    |
|                     |        | Subgraph             |
+---------------------+        +----------------------+
         ↑                               ↓
         |                      +----------------------+
         |                      | Azure Event Grid     |
         |                      +----------------------+
         |                               ↓
         |                      +----------------------+
         |                      | Function Apps        |
         |                      +----------------------+
         ↓                               ↓
+---------------------+        +----------------------+
| Pinax SDK           | <----> | ML Engine &          |
| (Cross-Chain Ops)   |        | Risk Analysis        |
+---------------------+        +----------------------+
```

## Integration Components

### EtherLinkSDK

The `EtherLinkSDK` in the `shared` directory provides a compatibility layer for interacting with EtherLink. It handles:

- Contract deployment and interaction
- Transaction signing and submission
- Event monitoring and filtering
- Cross-chain message passing
- Gas estimation and optimization

### Goldsky EtherLink Subgraph

The EtherLink-specific subgraphs in the `goldsky/etherlink` directory index and monitor:

- Smart contract deployments
- Transaction events
- Token transfers and approvals
- Custom contract events
- Protocol-level state changes

### Pinax SDK Integration

The Pinax SDK provides unified access to EtherLink alongside other supported chains, enabling:

- Single-interface multi-chain operations
- Cross-chain transaction bundling
- Unified wallet connection
- Consistent data models across chains

## Getting Started

### Prerequisites

- Access to an EtherLink RPC endpoint
- EtherLink testnet or mainnet account with funds
- Goldsky account for subgraph deployment
- Azure subscription for infrastructure deployment

### Environment Setup

Add the following environment variables to your local development environment or Azure configuration:

```
# EtherLink Configuration
ETHERLINK_RPC_URL=https://mainnet.etherlink.com/rpc
ETHERLINK_CHAIN_ID=1729
ETHERLINK_EXPLORER_URL=https://explorer.etherlink.com
ETHERLINK_WEBSOCKET_URL=wss://mainnet.etherlink.com/ws

# For testnet
ETHERLINK_TESTNET_RPC_URL=https://testnet.etherlink.com/rpc
ETHERLINK_TESTNET_CHAIN_ID=17290
```

### Installation

The EtherLink SDK is included in the repository. To use it in a new Function App:

1. Add a reference to the shared project in your Function App's `.csproj` file:

```xml
<ItemGroup>
  <ProjectReference Include="..\..\shared\EtherLinkSDK\EtherLinkSDK.csproj" />
</ItemGroup>
```

2. Register the EtherLink services in your startup configuration:

```csharp
builder.Services.AddEtherLinkServices(builder.Configuration);
```

## SDK Usage

### Initializing the SDK

```csharp
using VeritasVault.Shared.EtherLinkSDK;
using VeritasVault.Shared.EtherLinkSDK.Models;

// In your function or service
public class EtherLinkService
{
    private readonly IEtherLinkClient _etherLinkClient;

    public EtherLinkService(IEtherLinkClient etherLinkClient)
    {
        _etherLinkClient = etherLinkClient;
    }

    // Service methods...
}
```

### Querying Balances

```csharp
public async Task<decimal> GetTokenBalance(string tokenAddress, string walletAddress)
{
    var balance = await _etherLinkClient.GetERC20Balance(tokenAddress, walletAddress);
    return balance;
}
```

### Listening for Events

```csharp
public async Task SubscribeToTransfers(string tokenAddress, Action<TransferEvent> callback)
{
    await _etherLinkClient.SubscribeToERC20Transfers(tokenAddress, (sender, recipient, amount) => {
        callback(new TransferEvent
        {
            From = sender,
            To = recipient,
            Amount = amount
        });
    });
}
```

### Cross-Chain Operations

```csharp
public async Task<string> BridgeAssets(string fromAddress, string toAddress, decimal amount)
{
    var bridgeParams = new BridgeParams
    {
        SourceChain = Chain.Ethereum,
        DestinationChain = Chain.EtherLink,
        TokenAddress = "0x...",
        Amount = amount,
        Recipient = toAddress
    };

    return await _etherLinkClient.BridgeTokens(bridgeParams);
}
```

## Goldsky Subgraph Setup

### EtherLink Subgraph Configuration

Create your EtherLink subgraph definition in `src/goldsky/etherlink/schema.graphql`:

```graphql
type VaultTransaction @entity {
  id: ID!
  txHash: String!
  blockNumber: BigInt!
  timestamp: BigInt!
  from: String!
  to: String!
  value: BigInt!
  gasUsed: BigInt!
  gasPrice: BigInt!
  status: Boolean!
  methodId: String
  methodName: String
}

type VaultEvent @entity {
  id: ID!
  txHash: String!
  blockNumber: BigInt!
  timestamp: BigInt!
  contract: String!
  eventName: String!
  parameters: [EventParameter!]!
}

type EventParameter @entity {
  id: ID!
  name: String!
  value: String!
  valueType: String!
  indexed: Boolean!
}
```

### Subgraph Deployment

Deploy your EtherLink subgraph using the Goldsky CLI:

```bash
cd src/goldsky/etherlink
goldsky subgraph deploy veritasvault/etherlink-mainnet \
  --network etherlink-mainnet \
  --from-config subgraph.yaml
```

### Webhook Configuration

Configure the Goldsky webhook to send events to your Azure Event Grid:

```bash
goldsky subgraph webhook create veritasvault/etherlink-mainnet \
  --endpoint https://your-event-grid-endpoint.azure.com \
  --secret $WEBHOOK_SECRET \
  --events VaultTransaction,VaultEvent
```

## Cross-Chain Operations

### EtherLink-Tezos Bridge

The EtherLink SDK provides methods for bridging assets between EtherLink and Tezos:

```csharp
// Bridge ERC-20 token to Tezos FA2 token
public async Task<string> BridgeToTezos(string tokenAddress, string tezosAddress, decimal amount)
{
    var bridgeParams = new TezosEtherLinkBridgeParams
    {
        EthereumTokenAddress = tokenAddress,
        TezosAddress = tezosAddress,
        Amount = amount
    };

    return await _etherLinkClient.BridgeToTezos(bridgeParams);
}

// Bridge Tezos FA2 token to EtherLink ERC-20
public async Task<string> BridgeFromTezos(string tokenAddress, string etherLinkAddress, decimal amount)
{
    var bridgeParams = new TezosEtherLinkBridgeParams
    {
        TezosTokenAddress = tokenAddress,
        EthereumAddress = etherLinkAddress,
        Amount = amount
    };

    return await _etherLinkClient.BridgeFromTezos(bridgeParams);
}
```

### EtherLink-Ethereum Bridge

For bridging between EtherLink and Ethereum mainnet:

```csharp
public async Task<string> BridgeToEthereum(string tokenAddress, string ethereumAddress, decimal amount)
{
    var bridgeParams = new EthereumEtherLinkBridgeParams
    {
        EtherLinkTokenAddress = tokenAddress,
        EthereumAddress = ethereumAddress,
        Amount = amount
    };

    return await _etherLinkClient.BridgeToEthereum(bridgeParams);
}
```

### Multi-Chain Transaction Bundling

Using Pinax SDK with EtherLink for atomic multi-chain operations:

```csharp
public async Task<string> ExecuteMultiChainOperation(MultiChainOperationParams params)
{
    // Create a transaction bundle
    var bundle = _pinaxClient.CreateTransactionBundle();

    // Add EtherLink transaction
    bundle.AddEtherLinkTransaction(new EtherLinkTransactionParams
    {
        To = params.EtherLinkContractAddress,
        Value = 0,
        Data = params.EtherLinkCalldata
    });

    // Add Tezos transaction
    bundle.AddTezosTransaction(new TezosTransactionParams
    {
        To = params.TezosContractAddress,
        Amount = params.TezosAmount,
        Entrypoint = params.TezosEntrypoint,
        Parameters = params.TezosParameters
    });

    // Execute the bundle atomically
    return await _pinaxClient.ExecuteBundle(bundle);
}
```

## Security Considerations

### Optimistic Rollup Security Model

EtherLink uses an optimistic rollup architecture with a 7-day challenge period. Consider this when:

- Processing high-value transactions
- Implementing time-sensitive operations
- Designing cross-chain protocols

Implement appropriate waiting periods for large withdrawals and critical operations.

### Cross-Chain Security

When working with cross-chain operations:

1. Implement robust transaction verification
2. Use the Pinax SDK's atomic execution capabilities
3. Verify bridge transactions on both source and destination chains
4. Implement transaction monitoring and alerting

### Smart Contract Compatibility

While EtherLink is EVM-compatible, there are some differences to consider:

1. Gas costs may differ from Ethereum mainnet
2. Some precompiled contracts may have different addresses
3. Block times and confirmation counts differ
4. Some Ethereum opcodes may have different implementations

Always test contracts thoroughly on EtherLink testnet before deployment.

## Performance Optimization

### Gas Optimization

EtherLink gas prices are significantly lower than Ethereum mainnet, but optimization is still important:

1. Batch transactions when possible
2. Use efficient data structures
3. Minimize on-chain storage
4. Implement gas price estimation for optimal transaction timing

### Latency Considerations

EtherLink has different block times and finality characteristics:

- Block time: ~2 seconds
- Soft finality: ~30 seconds (Tezos finality)
- Hard finality: 7 days (challenge period)

Design your application to account for these timing differences.

## Troubleshooting

### Common Issues

#### Transaction Failures

If transactions fail:

1. Check gas limits and prices
2. Verify nonce management
3. Ensure contract compatibility
4. Check for sufficient balances

#### Bridge Delays

If bridge operations are delayed:

1. Verify transaction confirmation on source chain
2. Check bridge contract status
3. Confirm destination chain is operational
4. Check for bridge liquidity issues

#### Subgraph Synchronization

If Goldsky subgraphs are not synchronizing:

1. Check EtherLink RPC endpoint status
2. Verify subgraph deployment
3. Check for schema compatibility issues
4. Ensure webhook configuration is correct

### Support Resources

- EtherLink Discord: [discord.gg/etherlink](https://discord.gg/etherlink)
- EtherLink Documentation: [docs.etherlink.com](https://docs.etherlink.com)
- Goldsky Support: [support.goldsky.com](https://support.goldsky.com)
- Pinax Documentation: [docs.pinax.network](https://docs.pinax.network)

## Appendix: Technical Specifications

### EtherLink Network Parameters (2025)

| Parameter | Value |
|-----------|-------|
| Chain ID | 1729 |
| Block Time | ~2 seconds |
| Gas Limit | 30,000,000 |
| Average Gas Price | 0.08 gwei |
| Transaction Finality | 7 days (challenge period) |
| Soft Finality | ~30 seconds (Tezos finality) |
| Native Token | ETL |
| EVM Version | London |
| RPC Endpoint | https://mainnet.etherlink.com/rpc |
| WebSocket Endpoint | wss://mainnet.etherlink.com/ws |
| Explorer | https://explorer.etherlink.com |

### Supported Contract Standards

| Standard | Support Level | Notes |
|----------|--------------|-------|
| ERC-20 | Full | Complete compatibility |
| ERC-721 | Full | Complete compatibility |
| ERC-1155 | Full | Complete compatibility |
| ERC-4626 | Full | Complete compatibility |
| ERC-2612 | Full | Permit functionality supported |
| ERC-2981 | Full | Royalty standard supported |
| ERC-165 | Full | Interface detection supported |
| ERC-777 | Partial | Some hooks may behave differently |
| ERC-3156 | Full | Flash loans supported |

### Bridge Limitations

| Parameter | Limit |
|-----------|-------|
| Maximum Bridge Amount | 1,000,000 USD equivalent |
| Minimum Bridge Amount | 1 USD equivalent |
| Bridge Fee | 0.1% |
| Bridge Delay (EtherLink to Ethereum) | ~30 minutes |
| Bridge Delay (Ethereum to EtherLink) | ~10 minutes |
| Bridge Delay (EtherLink to Tezos) | ~5 minutes |
| Bridge Delay (Tezos to EtherLink) | ~5 minutes |
