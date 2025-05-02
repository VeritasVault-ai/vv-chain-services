# vv-chain-services
VeritasVault.ai vv-chain-services

## Repo structure

### 4. vv-chain-services
Blockchain integration and event processing services

```
vv-chain-services/
├── .github/
│   └── workflows/       # CI/CD pipelines for Azure Functions
├── src/
│   ├── functions/       # Azure Functions
│   │   ├── RiskBot/     # LTV and TVL calculations
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

---

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

### ♻️ Benefits

- Fully decoupled, scalable event pipeline
- Multiple independent consumers
- High resilience with Event Grid retries
- Goldsky handles chain-to-cloud reliably
- Cosmos DB replaces the need for Postgres
- Secure, observable, and DevOps-friendly

