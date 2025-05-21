version: '3.8'

services:
  devcontainer:
    build: 
      context: .
      dockerfile: Dockerfile
    volumes:
      - ..:/workspace:cached
      - ~/.gitconfig:/home/vscode/.gitconfig:cached
      - ~/.ssh:/home/vscode/.ssh:cached
      - ~/.azure:/home/vscode/.azure:cached
    command: sleep infinity
    depends_on:
      - redis
    ports:
      - "7071:7071"
      - "8000:8000"
      - "5000-5001:5000-5001"
    environment:
      - AZURE_FUNCTIONS_ENVIRONMENT=Development
      - ML_ENDPOINT=http://localhost:8000/predict
      - REDIS_CONNECTION_STRING=redis:6379
      - DOTNET_NOLOGO=true
      - DOTNET_CLI_TELEMETRY_OPTOUT=1
    networks:
      - dev-network
    restart: unless-stopped
  redis:
    image: redis:alpine
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - dev-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

networks:
  dev-network:
    driver: bridge

volumes:
  redis-data:
