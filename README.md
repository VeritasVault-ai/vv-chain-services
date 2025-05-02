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

