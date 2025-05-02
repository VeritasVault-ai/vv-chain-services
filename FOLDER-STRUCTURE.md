# VeritasVault Project Structure

This document provides a detailed explanation of the repository structure for both the `vv-chain-services` project and the broader VeritasVault ecosystem.

## Table of Contents

- [Repository Ecosystem Overview](#repository-ecosystem-overview)
- [vv-chain-services Structure](#vv-chain-services-structure)
  - [Root Directory](#root-directory)
  - [Function Apps](#function-apps)
  - [Shared Code](#shared-code)
  - [Goldsky Subgraphs](#goldsky-subgraphs)
  - [ML Engine](#ml-engine)
  - [Tests](#tests)
- [Related Repositories](#related-repositories)
  - [vv-iac](#vv-iac)
  - [vv-docs](#vv-docs)
  - [vv-landing](#vv-landing)
  - [vv-game](#vv-game)

## Repository Ecosystem Overview

The VeritasVault platform is organized into several repositories, each with a specific purpose and responsibility. This modular approach allows for:

1. **Clear Separation of Concerns**: Each repository has a well-defined responsibility
2. **Independent Development Cycles**: Teams can work on different components without interference
3. **Specialized CI/CD Pipelines**: Each repository can have tailored build and deployment processes
4. **Granular Access Control**: Repository permissions can be managed based on team roles
5. **Focused Issue Tracking**: Issues and feature requests can be tracked in the relevant repository

The VeritasVault ecosystem consists of the following repositories:

| Repository | Purpose |
|------------|---------|
| `vv-chain-services` | Core blockchain integration and event processing services |
| `vv-iac` | Infrastructure as Code for all VeritasVault services |
| `vv-docs` | Comprehensive documentation for the platform |
| `vv-landing` | Public-facing website and marketing materials |
| `vv-game` | Gamification elements and interactive experiences |

## vv-chain-services Structure

### Root Directory

```
vv-chain-services/
├── .github/                      # GitHub workflows and configuration
├── .gitignore                    # Git ignore file
├── package.json                  # Root package.json for workspace management
├── docs/                         # Local documentation (duplicated from vv-docs)
├── src/                          # Source code
├── tests/                        # Test code
└── README.md                     # Main README
```

### Function Apps

```
src/function-apps/
├── RiskBotApp/                   # Risk calculation and ML integration
│   ├── RiskBotFunction.cs        # Main Azure Function
│   ├── RiskApiClient.cs          # Client for ML Engine API
│   ├── Models.cs                 # Data contracts
│   ├── Helpers.cs                # Utility functions
│   ├── host.json                 # Function App host configuration
│   └── local.settings.json       # Local settings (gitignored)
│
├── MetricsFunctionApp/           # OpenTelemetry metrics publishing
│   ├── MetricsBotFunction.cs     # Main function
│   ├── TelemetryService.cs       # Service for sending telemetry
│   ├── host.json                 # Function configuration
│   └── local.settings.json       # Local settings (gitignored)
│
├── AlertFunctionApp/             # Notification triggers
│   ├── AlertFunction.cs          # Main function
│   ├── NotificationService.cs    # Service for sending notifications
│   ├── host.json                 # Function configuration
│   └── local.settings.json       # Local settings (gitignored)
│
└── ArchivalFunctionApp/          # Data storage operations
    ├── ArchivalFunction.cs       # Main function
    ├── StorageService.cs         # Service for data storage
    ├── host.json                 # Function configuration
    └── local.settings.json       # Local settings (gitignored)
```

### Shared Code

```
src/shared/
├── models/                       # Data models
│   ├── EventModels.cs            # Models for blockchain events
│   └── DomainModels.cs           # Domain-specific models
│
├── services/                     # Service integrations
│   ├── CosmosDbService.cs        # Cosmos DB integration
│   ├── RedisService.cs           # Redis cache integration
│   └── KeyVaultService.cs        # Key Vault integration
│
└── utils/                        # Helper functions
    ├── EventGridHelpers.cs       # Event Grid utilities
    └── TelemetryHelpers.cs       # Telemetry utilities
```

### Goldsky Subgraphs

```
src/goldsky/
├── .goldsky-version              # Track Goldsky CLI version used
├── subgraph.config.yml           # Configuration for multiple GraphQL schemas
├── tezos/                        # Tezos-specific subgraphs
│   └── schema.graphql            # GraphQL schema for Tezos
└── evm/                          # EVM-specific subgraphs
    └── schema.graphql            # GraphQL schema for EVM
```

### ML Engine

```
src/ml-engine/
├── app/
│   ├── main.py                   # FastAPI app
│   ├── models/                   # ML models (pickle / joblib / ONNX)
│   ├── services/                 # Risk calculations
│   ├── schemas/                  # Input/output Pydantic schemas
│   └── utils/                    # Normalizers, scorers, etc.
├── tests/                        # Python-specific tests
│   ├── test_risk_calculations.py
│   └── test_api.py
├── requirements.txt              # Python dependencies
├── Dockerfile                    # ML Engine container definition
└── package.json                  # Node.js dependencies for ML Engine
```

### Tests

```
tests/
├── RiskBotTests/
│   ├── RiskBotFunctionTests.cs   # Tests for RiskBotFunction
│   └── RiskApiClientTests.cs     # Tests for RiskApiClient
├── MetricsFunctionTests/         # Tests for MetricsFunctionApp
├── AlertFunctionTests/           # Tests for AlertFunctionApp
└── ArchivalFunctionTests/        # Tests for ArchivalFunctionApp
```

## Related Repositories

### vv-iac

The `vv-iac` (Infrastructure as Code) repository contains all the infrastructure definitions for the VeritasVault platform. This approach allows for:

- **Centralized Infrastructure Management**: All infrastructure definitions are in one place
- **Consistent Deployment Patterns**: Common deployment patterns can be reused across services
- **Environment Parity**: Development, staging, and production environments can be kept in sync
- **Infrastructure Versioning**: Changes to infrastructure can be tracked and rolled back if needed
- **Cross-Service Dependencies**: Dependencies between services can be managed in one place

```
vv-iac/
├── .github/
│   └── workflows/                # CI/CD pipelines for infrastructure
│       ├── risk-function-ci.yml  # Separate CI/CD for Risk Function App
│       ├── alert-function-ci.yml # Separate CI/CD for Alert Function App
│       ├── metrics-function-ci.yml # Separate CI/CD for Metrics Function App
│       ├── archival-function-ci.yml # Separate CI/CD for Archival Function App
│       └── ml-engine-ci.yml      # CI/CD for Python ML Engine
├── infra/                      
│   ├── bicep/                    # Bicep templates
│   │   ├── main.bicep            # Main deployment template
│   │   ├── eventgrid.bicep       # Event Grid resources
│   │   ├── functions.bicep       # Function Apps
│   │   ├── storage.bicep         # Storage resources
│   │   ├── monitoring.bicep      # Monitoring resources
│   │   ├── api-gateway.bicep     # API Gateway for ML Engine isolation
│   │   └── ml-engine.bicep       # ML Engine infrastructure
│   └── scripts/                  # Deployment scripts
│       ├── deploy.ps1            # Deployment scripts
│       └── setup-goldsky.sh      # Goldsky setup script
├── tests/                        # Infrastructure tests
└── bicep-linter.yml              # Bicep linting configuration
```

### vv-docs

The `vv-docs` repository contains comprehensive documentation for the VeritasVault platform. This approach allows for:

- **Centralized Documentation**: All documentation is in one place
- **Consistent Documentation Style**: Documentation can follow a consistent style and format
- **Documentation Versioning**: Changes to documentation can be tracked and rolled back if needed
- **Cross-Service Documentation**: Documentation that spans multiple services can be managed in one place
- **Documentation CI/CD**: Documentation can be automatically built and deployed to a documentation site

```
vv-docs/
├── .github/
│   └── workflows/                # CI/CD pipelines for documentation
├── architecture/                 # Architecture documentation
│   ├── overview.md               # System overview
│   ├── chain-services.md         # Chain services architecture
│   └── diagrams/                 # Architecture diagrams
├── api/                          # API documentation
│   ├── risk-bot.md               # Risk Bot API
│   └── ml-engine.md              # ML Engine API
├── user-guides/                  # User guides
├── developer-guides/             # Developer guides
│   ├── getting-started.md        # Getting started guide
│   ├── local-development.md      # Local development guide
│   └── contributing.md           # Contributing guide
└── deployment/                   # Deployment guides
```

### vv-landing

The `vv-landing` repository contains the public-facing website and marketing materials for the VeritasVault platform. This approach allows for:

- **Independent Website Development**: The website can be developed independently of the core services
- **Marketing-Focused Content**: Content can be tailored for marketing purposes
- **Rapid Iteration**: The website can be updated quickly without affecting core services
- **Specialized Team**: A dedicated team can work on the website without needing access to core services
- **Different Technology Stack**: The website can use a different technology stack than the core services

```
vv-landing/
├── .github/
│   └── workflows/                # CI/CD pipelines for website
├── public/                       # Static assets
│   ├── images/                   # Images
│   ├── videos/                   # Videos
│   └── documents/                # Downloadable documents
├── src/                          # Website source code
│   ├── components/               # React components
│   ├── pages/                    # Next.js pages
│   ├── styles/                   # CSS styles
│   └── utils/                    # Utility functions
├── content/                      # Marketing content
│   ├── blog/                     # Blog posts
│   ├── case-studies/             # Case studies
│   └── product/                  # Product information
└── package.json                  # Node.js dependencies
```

### vv-game

The `vv-game` repository contains gamification elements and interactive experiences for the VeritasVault platform. This approach allows for:

- **Specialized Game Development**: Game development can be done by a specialized team
- **Different Technology Stack**: Games can use a different technology stack than the core services
- **Independent Release Cycle**: Games can be released on a different schedule than the core services
- **Resource-Intensive Development**: Game development often requires different resources than core services
- **Cross-Platform Support**: Games may need to support different platforms than the core services

```
vv-game/
├── .github/
│   └── workflows/                # CI/CD pipelines for games
├── assets/                       # Game assets
│   ├── images/                   # Images
│   ├── audio/                    # Audio files
│   └── models/                   # 3D models
├── src/                          # Game source code
│   ├── components/               # Game components
│   ├── scenes/                   # Game scenes
│   ├── utils/                    # Utility functions
│   └── main.js                   # Main game entry point
├── blockchain/                   # Blockchain integration
│   ├── contracts/                # Smart contracts
│   └── integration/              # Integration with vv-chain-services
└── package.json                  # Node.js dependencies
```

## Repository Structure Rationale

The VeritasVault ecosystem is divided into multiple repositories for several key reasons:

### 1. Separation of Concerns

Each repository has a clear and distinct purpose:

- **vv-chain-services**: Core blockchain integration and event processing services
- **vv-iac**: Infrastructure as Code for all VeritasVault services
- **vv-docs**: Comprehensive documentation for the platform
- **vv-landing**: Public-facing website and marketing materials
- **vv-game**: Gamification elements and interactive experiences

This separation ensures that changes in one area don't affect others unnecessarily.

### 2. Team Specialization

Different teams can focus on their areas of expertise:

- **Blockchain Team**: Works primarily in vv-chain-services
- **DevOps Team**: Works primarily in vv-iac
- **Documentation Team**: Works primarily in vv-docs
- **Marketing Team**: Works primarily in vv-landing
- **Game Development Team**: Works primarily in vv-game

### 3. Technology Stack Differences

Different components may require different technology stacks:

- **vv-chain-services**: .NET and Python
- **vv-iac**: Bicep and PowerShell
- **vv-docs**: Markdown and documentation tools
- **vv-landing**: React, Next.js, and marketing tools
- **vv-game**: Game engines and WebGL

### 4. Release Cycle Independence

Different components may have different release cycles:

- **vv-chain-services**: May release based on blockchain updates or new features
- **vv-iac**: May release based on infrastructure changes or optimizations
- **vv-docs**: May release based on documentation updates or new features
- **vv-landing**: May release based on marketing campaigns or content updates
- **vv-game**: May release based on game updates or new features

### 5. Security and Access Control

Different repositories may have different security requirements:

- **vv-chain-services**: May contain sensitive code or configurations
- **vv-iac**: May contain infrastructure secrets or sensitive configurations
- **vv-docs**: May be more widely accessible for documentation contributors
- **vv-landing**: May be accessible to marketing and content teams
- **vv-game**: May be accessible to game developers and designers

### 6. Repository Size and Performance

Splitting the codebase into multiple repositories helps manage repository size and performance:

- Smaller repositories are faster to clone and work with
- Smaller repositories have faster CI/CD pipelines
- Smaller repositories have more focused issue tracking

### 7. Dependency Management

Different components may have different dependency requirements:

- **vv-chain-services**: May depend on blockchain libraries and ML frameworks
- **vv-iac**: May depend on infrastructure tools and cloud provider SDKs
- **vv-docs**: May depend on documentation generators and tools
- **vv-landing**: May depend on web frameworks and marketing tools
- **vv-game**: May depend on game engines and graphics libraries

By separating these concerns into different repositories, we can manage dependencies more effectively and avoid conflicts.