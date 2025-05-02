# VeritasVault Risk Bot

This project contains a risk prediction system for blockchain vaults, consisting of:

1. **RiskBotApp** - An Azure Function (.NET) that processes blockchain events
2. **ml-engine** - A Python FastAPI service for risk prediction

## Development Environment

This project uses Visual Studio Code Dev Containers for a consistent development experience.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Getting Started

1. Clone the repository
2. Open the project in VS Code
3. When prompted, click "Reopen in Container" or run the "Remote-Containers: Reopen in Container" command
4. The container will build and set up the development environment

### Running the Project Locally

#### Start the ML Engine

```bash
cd ml-engine
uvicorn app.main:app --reload --port 8000
```

#### Start the Azure Function

```bash
cd RiskBotApp
func start
```

### Project Structure

```
vv-chain-services/
├── RiskBotApp/                   # Azure Function App (.NET)
│   ├── Models/
│   │   ├── EventModels.cs        # Blockchain event models
│   │   └── DomainModels.cs       # Risk prediction models
│   ├── RiskBotFunction.cs        # Event Grid trigger function
│   ├── RiskApiClient.cs          # Client for ML-Engine API
│   ├── Helpers.cs                # Utility functions
│   ├── Startup.cs                # DI configuration
│   ├── RiskBotApp.csproj         # Project file
│   ├── host.json                 # Function configuration
│   └── local.settings.json       # Local settings (gitignored)
│
└── ml-engine/                    # Python ML Engine (separate unit)
    ├── app/
    │   ├── main.py               # FastAPI app
    │   ├── models/               # ML models
    │   ├── services/             # Risk calculations
    │   ├── schemas/              # Pydantic schemas
    │   └── utils/                # Helper utilities
    ├── tests/                    # Python tests
    ├── requirements.txt          # Python dependencies
    ├── Dockerfile                # Container definition
    └── package.json              # Node.js dependencies
```

## Deployment

### Azure Function

```bash
cd RiskBotApp
func azure functionapp publish <function-app-name>
```

### ML Engine

The ML Engine can be deployed as a container to Azure Container Apps, Azure Kubernetes Service, or Azure App Service.

```bash
cd ml-engine
az acr build --registry <acr-name> --image ml-engine:latest .
```

## Testing

### .NET Tests

```bash
cd RiskBotApp
dotnet test
```

### Python Tests

```bash
cd ml-engine
pytest
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.