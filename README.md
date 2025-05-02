# vv-chain-services
Blockchain integration and event processing services

This repository contains the event-driven microservices responsible for ingesting, processing, analyzing, and archiving blockchain event data from Tezos and EVM networks. It is part of the VeritasVault.ai platform and is tightly integrated with Goldsky, Azure Event Grid, and a distributed risk intelligence engine powered by Python-based ML.

The solution is designed with resilience, observability, and modularity in mind — allowing independent teams to scale risk models, extend observability, or hook in new event sources with minimal friction.

## 📚 Table of Contents
- [🔧 Chain and Services Architecture](#-chain-and-services-architecture)
- [🔧 Repository Structure](#-repository-structure)
- [📀 Data Flow Overview](#-data-flow-overview)
- [⚖️ Azure Components](#-azure-components)
- [🎓 Use Case Handlers](#-use-case-handlers)
- [🔨 Goldsky Setup Notes](#-goldsky-setup-notes)
- [🌐 Security & Observability](#-security--observability)
- [♻️ Benefits](#-benefits)

```text

```

## Chain and Services Architecture

```mermaid
flowchart TB
  subgraph Blockchain["Blockchain Networks"]
      Tezos["Tezos Network"]
      EVM["EVM Networks"]
  end
  
  subgraph Goldsky["Goldsky Data Platform"]
      TezosSubgraph["Tezos Subgraph"]
      EVMSubgraph["EVM Subgraph"]
      WebhookOutput["Webhook Output"]
  end
  
  subgraph Azure["Azure Cloud"]
      EventGrid["Azure Event Grid Topic"]
      
      subgraph Functions["Azure Functions"]
          RiskBot["Risk Bot\n(LTV & TVL Calculations)"]
          MetricsBot["Metrics Bot\n(Prometheus Push)"]
          AlertFunction["Alert Function\n(Notifications)"]
          ArchivalFunction["Archival Function\n(Data Storage)"]
      end
      
      subgraph Storage["Storage & Caching"]
          CosmosDB["Cosmos DB\n(Long-term Storage)"]
          Redis["Redis Cache\n(Real-time Data)"]
          DeadLetter["Dead Letter Storage"]
      end
      
      subgraph Monitoring["Monitoring & Observability"]
          AppInsights["Application Insights"]
          LogAnalytics["Log Analytics"]
          OpenTelemetry["OpenTelemetry\nCollector"]
          SecurityCenter["Security Center"]
      end
      
      subgraph Notifications["Notification Channels"]
          Teams["Microsoft Teams"]
          Email["Email"]
          SMS["SMS"]
          LogicApp["Logic App\n(Workflow)"]
      end
      
      subgraph Security["Security Components"]
          KeyVault["Azure Key Vault"]
          ManagedIdentity["Managed Identities"]
      end
  end
  
  subgraph Consumers["Data Consumers"]
      Dashboard["Real-time Dashboard"]
      GameSuite["DeFi Breakout Game"]
      RiskEngine["Risk Management Engine"]
  end
  
  %% Connections
  Tezos --> TezosSubgraph
  EVM --> EVMSubgraph
  TezosSubgraph --> WebhookOutput
  EVMSubgraph --> WebhookOutput
  WebhookOutput --> EventGrid
  
  EventGrid --> RiskBot
  EventGrid --> MetricsBot
  EventGrid --> AlertFunction
  EventGrid --> ArchivalFunction
  
  RiskBot --> Redis
  RiskBot --> OpenTelemetry
  MetricsBot --> OpenTelemetry
  AlertFunction --> LogicApp
  LogicApp --> Teams
  LogicApp --> Email
  LogicApp --> SMS
  ArchivalFunction --> CosmosDB
  
  EventGrid -.-> DeadLetter
  DeadLetter -.-> SecurityCenter
  
  Functions --> AppInsights
  AppInsights --> LogAnalytics
  OpenTelemetry --> LogAnalytics
  
  Functions --> KeyVault
  Functions -.-> ManagedIdentity
  ManagedIdentity --> KeyVault
  
  Redis --> Dashboard
  Redis --> GameSuite
  Redis --> RiskEngine
  CosmosDB -.-> Dashboard
  
  classDef blockchain fill:#d1c4e9,stroke:#5e35b1,stroke-width:2px,color:#1a237e
  classDef goldsky   fill:#f8bbd0,stroke:#c2185b,stroke-width:1px,color:#880e4f
  classDef azure     fill:#bbdefb,stroke:#1976d2,stroke-width:1px,color:#0d47a1
  classDef function  fill:#c8e6c9,stroke:#388e3c,stroke-width:1px,color:#1b5e20
  classDef storage   fill:#fff9c4,stroke:#fbc02d,stroke-width:1px,color:#f57f17
  classDef monitoring fill:#b2ebf2,stroke:#00acc1,stroke-width:1px,color:#006064
  classDef notification fill:#f3e5f5,stroke:#8e24aa,stroke-width:1px,color:#4a148c
  classDef security  fill:#ffcdd2,stroke:#e53935,stroke-width:1px,color:#b71c1c
  classDef consumer  fill:#dcedc8,stroke:#7cb342,stroke-width:1px,color:#33691e
  
  class Tezos,EVM blockchain
  class TezosSubgraph,EVMSubgraph,WebhookOutput goldsky
  class EventGrid azure
  class RiskBot,MetricsBot,AlertFunction,ArchivalFunction function
  class CosmosDB,Redis,DeadLetter storage
  class AppInsights,LogAnalytics,OpenTelemetry,SecurityCenter monitoring
  class Teams,Email,SMS,LogicApp notification
  class KeyVault,ManagedIdentity security
  class Dashboard,GameSuite,RiskEngine consumer
```

## 🔧 Repository Structure

```
vv-iac/                                # Separate repo - Infrastructure as Code
├── .github/
│   └── workflows/                     # CI/CD pipelines for Azure Functions and ML Engine
│       ├── risk-function-ci.yml       # Separate CI/CD for Risk Function App
│       ├── alert-function-ci.yml      # Separate CI/CD for Alert Function App
│       ├── metrics-function-ci.yml    # Separate CI/CD for Metrics Function App
│       ├── archival-function-ci.yml   # Separate CI/CD for Archival Function App
│       └── ml-engine-ci.yml           # CI/CD for Python ML Engine
├── infra/                      
│   ├── bicep/
│   │   ├── main.bicep                # Main deployment template
│   │   ├── eventgrid.bicep           # Event Grid resources
│   │   ├── functions.bicep           # Function Apps
│   │   ├── storage.bicep             # Storage resources
│   │   ├── monitoring.bicep          # Monitoring resources
│   │   ├── api-gateway.bicep         # New: API Gateway for ML Engine isolation
│   │   └── ml-engine.bicep           # New: Separate ML Engine infrastructure
│   └── scripts/
│       ├── deploy.ps1                # Deployment scripts
│       └── setup-goldsky.sh          # Goldsky setup script
├── tests/                            # New: Infrastructure tests
├── bicep-linter.yml                  # Bicep linting configuration
      └── whatif-tests.ps1            # WhatIf tests for infrastructure changes


vv-chain-services/
├── .gitignore                    # Ensure local.settings.json is excluded
├── package.json                  # Root package.json for workspace management
├── src/
│   ├── function-apps/               # Separated Function Apps for independent scaling/SLAs
│   │   ├── RiskBotApp/              # Renamed from RiskFunctionApp to align with internal naming
│   │   │   ├── RiskBotFunction.cs       # Main Azure Function
│   │   │   ├── RiskApiClient.cs         # Calls Python ML engine
│   │   │   ├── Models.cs                # Data contracts
│   │   │   ├── Helpers.cs
│   │   │   ├── host.json               # Function App host configuration
│   │   │   └── local.settings.json  # Will be excluded via .gitignore
│   │   ├── MetricsFunctionApp/  # OpenTelemetry metrics publishing
│   │   │   ├── MetricsBotFunction.cs
│   │   │   ├── TelemetryService.cs
│   │   │   ├── host.json
│   │   │   └── local.settings.json  # Will be excluded via .gitignore
│   │   ├── AlertFunctionApp/   # Notification triggers
│   │   │   ├── AlertFunction.cs
│   │   │   ├── NotificationService.cs
│   │   │   ├── host.json
│   │   │   └── local.settings.json  # Will be excluded via .gitignore
│   │   └── ArchivalFunctionApp/ # Data storage operations
│   │       ├── ArchivalFunction.cs
│   │       ├── StorageService.cs
│   │       ├── host.json
│   │       └── local.settings.json  # Will be excluded via .gitignore
│   ├── shared/                 # Shared code and utilities
│   │   ├── models/             # Data models
│   │   │   ├── EventModels.cs
│   │   │   └── DomainModels.cs
│   │   ├── services/           # Service integrations
│   │   │   ├── CosmosDbService.cs
│   │   │   ├── RedisService.cs
│   │   │   └── KeyVaultService.cs
│   │   └── utils/              # Helper functions
│   │       ├── EventGridHelpers.cs
│   │       └── TelemetryHelpers.cs
│   ├── goldsky/                # Goldsky subgraph definitions
│   │   ├── .goldsky-version      # Track Goldsky CLI version used
│   │   ├── subgraph.config.yml   # Configuration for multiple GraphQL schemas
│   │   ├── tezos/              # Tezos-specific subgraphs
│   │   │   └── schema.graphql
│   │   └── evm/                # EVM-specific subgraphs
│   │       └── schema.graphql
│   └── ml-engine/              # Python ML Engine (separate deployable unit)
│       ├── app/
│       │   ├── main.py         # FastAPI app
│       │   ├── models/         # ML models (pickle / joblib / ONNX)
│       │   ├── services/       # Risk calculations
│       │   ├── schemas/        # Input/output Pydantic schemas
│       │   └── utils/          # Normalizers, scorers, etc.
│       ├── tests/              # Python-specific tests
│       │   ├── test_risk_calculations.py
│       │   └── test_api.py
│       ├── requirements.txt    # Python dependencies
│       ├── Dockerfile          # ML Engine container definition
│       └── package.json        # Node.js dependencies for ML Engine
├── tests/                      # C# tests for Azure Functions
│   ├── RiskBotTests/
│   │   ├── RiskBotFunctionTests.cs
│   │   └── RiskApiClientTests.cs
│   ├── MetricsFunctionTests/
│   ├── AlertFunctionTests/
│   └── ArchivalFunctionTests/
└── README.md                   # Repository documentation

```

## 📀 Data Flow Overview

```
Blockchain (Tezos / EVM)
        ⬇️
    Goldsky Subgraph
        ⬇️
     [Webhook Output]
        ⬇️
Azure Event Grid Topic
        ⬇️
 +--------------------+----------------------+------------------+
 |                    |                      |                  |
 V                    V                      V                  V
Risk Bot         Metrics Bot         Alert Function      Archival Function
(Estimates, LTV) (OpenTelemetry)     (Notify, Email)     (Store to Cosmos DB)
```

## ⚖️ Azure Components

| Component              | Purpose                                                      |
|------------------------|--------------------------------------------------------------|
| Event Grid Topic       | Central hub for blockchain event publications                |
| Event Subscriptions    | Routes Goldsky event data to various handlers                |
| Azure Function Apps    | Stateless logic (risk calculations, alert triggers)          |
| Azure Queue (optional) | Buffer layer if retries/delays are needed                    |
| Cosmos DB              | Long-term archival of structured indexed events              |
| Redis                  | Shared memory cache for downstream services                  |
| OpenTelemetry          | Unified observability for metrics, traces, and logs          |
| Azure Monitor / Log Analytics | Logs and telemetry aggregation for debugging and insight |

## 🎓 Use Case Handlers

**Risk Function App:**
- Triggers on new asset price updates
- Recalculates portfolio LTV and TVL
- Publishes to Redis for dashboard
- Communicates with ML Engine for risk analysis

**Metrics Function App:**
- Extracts event type and timing
- Publishes metrics via OpenTelemetry
- Monitors system health and performance

**Alert Function App:**
- If LTV > threshold or abnormal TXs
- Sends to Teams / Email / SMS (via Logic App)
- Handles notification throttling and aggregation

**Archival Function App:**
- Batches and stores full JSON payloads
- Writes to Cosmos DB with TTL
- Manages data partitioning and indexing

## 🔨 Goldsky Setup Notes

- Use `webhook` target type (POST)
- Payload format: JSON
- Use filtering logic in subgraph to minimize spam
- Include retry logic on failed webhook delivery (Goldsky handles retries)
- Include event signatures and timestamps for deduplication

## 🌐 Security & Observability

- All endpoints authenticated with Managed Identity
- Each Function App has its own Managed Identity with specific RBAC permissions
- OpenTelemetry integration for unified observability
- Event Grid Dead Letter Queue for failed delivery tracking
- Alerts routed to Security Center if abnormal spike in payloads
- Key Vault integration for secure secret management

## ♻️ Benefits of This Architecture

#### **Decoupled Processing:**
Each Function App operates independently, allowing for flexible scaling and deployment

#### **High Resilience:**
Event Grid provides reliable delivery with retries and dead letter queues

#### **Scalable:**
Can handle increasing volumes of blockchain events as the platform grows

#### **Observable:**
Comprehensive logging and monitoring throughout the pipeline

#### **Secure:**
Managed Identities and Key Vault integration for secure secret management

#### **DevOps-Friendly:**
Infrastructure as Code (Bicep) for repeatable deployments

#### **Independent Scaling:**
Each Function App can scale based on its specific workload and requirements
