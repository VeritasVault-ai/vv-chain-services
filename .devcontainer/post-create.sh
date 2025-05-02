#!/bin/bash
set -e

echo "Setting up development environment..."

# Install .NET dependencies
echo "Restoring .NET dependencies..."
if [ -f "function-apps/RiskBotApp.csproj" ]; then
  cd function-apps
  dotnet restore
  cd ..
fi

# Install Python dependencies
echo "Installing Python dependencies..."
if [ -f "src/ml-engine/requirements.txt" ]; then
  cd src/ml-engine
  pip install -r requirements.txt
  cd ../..
fi

# Install Node.js dependencies if needed
if [ -f "src/ml-engine/package.json" ]; then
  cd src/ml-engine
  npm install
  cd ../..
fi

echo "Creating local settings files if they don't exist..."

# Create local.settings.json for Azure Functions if it doesn't exist
if [ ! -f "function-apps/local.settings.json" ]; then
  cat > function-apps/local.settings.json << EOF
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet",
    "ML_ENDPOINT": "http://localhost:8000/predict",
    "REDIS_CONNECTION_STRING": "localhost:6379"
  }
}
EOF
  echo "Created function-apps/local.settings.json"
fi

echo "Development environment setup complete!"