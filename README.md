# 4. vv-chain-services
Blockchain integration and event processing services

## Repo structure

```
vv-chain-services/
├── .github/
│   └── workflows/       # CI/CD pipelines for Azure Functions
├── src/
│   ├── functions/       # Azure Functions
│   │   ├── RiskBot/     # LTV and TVL calculations
<--- RiskBot could also be python in which case create subolder in src --->
│   │   ├── MetricsBot/  # Prometheus metrics publishing
│   │   ├── AlertFunc/   # Notification triggers
│   │   └── ArchivalFunc/# Data storage operations
│   ├── shared/          # Shared code and utilities
│   │   ├── models/      # Data models
│   │   ├── services/    # Service integrations
│   │   └── utils/       # Helper functions
│   └── goldsky/         # Goldsky subgraph definitions
│       ├── tezos/       # Tezos-specific subgraphs
│       └── evm/         # EVM-specific subgraphs
├── tests/               # Test suite
├── README.md            # Repository documentation
└── package.json         # Dependencies and scripts
```

**VeritasVault Event Grid Architecture (Goldsky Integration)**

``` mermaid
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
          Prometheus["Prometheus\nPushgateway"]
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
  MetricsBot --> Prometheus
  AlertFunction --> LogicApp
  LogicApp --> Teams
  LogicApp --> Email
  LogicApp --> SMS
  ArchivalFunction --> CosmosDB
  
  EventGrid -.-> DeadLetter
  DeadLetter -.-> SecurityCenter
  
  Functions --> AppInsights
  AppInsights --> LogAnalytics
  
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
  class EventGrid,Functions,Storage,Monitoring,Notifications,Security azure
  class RiskBot,MetricsBot,AlertFunction,ArchivalFunction function
  class CosmosDB,Redis,DeadLetter storage
  class AppInsights,LogAnalytics,Prometheus,SecurityCenter monitoring
  class Teams,Email,SMS,LogicApp notification
  class KeyVault,ManagedIdentity security
  class Dashboard,GameSuite,RiskEngine consumer
```

### 📀 Data Flow Overview

```text
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
(Estimates, LTV) (Prometheus Push)   (Notify, Email)     (Store to Cosmos DB)
```

---

### ⚖️ Key Azure Components

| Component              | Purpose                                                      |
|------------------------|--------------------------------------------------------------|
| Event Grid Topic       | Central hub for blockchain event publications                |
| Event Subscriptions    | Routes Goldsky event data to various handlers                |
| Azure Function         | Stateless logic (risk calculations, alert triggers)          |
| Azure Queue (optional) | Buffer layer if retries/delays are needed                    |
| Cosmos DB              | Long-term archival of structured indexed events              |
| Redis (optional)       | Shared memory cache for downstream services                  |
| Azure Monitor / Log Analytics | Logs and telemetry aggregation for debugging and insight |

---

### 🎓 Use Case Handlers

**Risk Bot:**
- Triggers on new asset price updates
- Recalculates portfolio LTV and TVL
- Publishes to Redis for dashboard

**Metrics Bot:**
- Extracts event type and timing
- Publishes to Prometheus via Pushgateway

**Alert Function:**
- If LTV > threshold or abnormal TXs
- Sends to Teams / Email / SMS (via Logic App)

**Archival Function:**
- Batches and stores full JSON payloads
- Writes to Cosmos DB or Azure Blob with TTL

---

### 🔨 Goldsky Setup Notes

- Use `webhook` target type (POST)
- Payload format: JSON
- Use filtering logic in subgraph to minimize spam
- Include retry logic on failed webhook delivery (Goldsky handles retries)
- Include event signatures and timestamps for deduplication

---

### 🌐 Security & Observability

- All endpoints authenticated with Managed Identity or signed tokens
- Use App Insights + Prometheus for observability
- Add Event Grid Dead Letter Queue for failed delivery tracking
- Alerts routed to Security Center if abnormal spike in payloads

---

### ♻️ Key Benefits of This Architecture
#### **Decoupled Processing:**
Each component operates independently, allowing for flexible scaling and deployment
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

