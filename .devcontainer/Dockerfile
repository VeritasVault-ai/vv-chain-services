FROM mcr.microsoft.com/devcontainers/dotnet:8.0

# 1) Install Python and venv support
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
         curl lsb-release gnupg software-properties-common \
         python3.11 python3.11-venv \
         git git-lfs \
    && rm -rf /var/lib/apt/lists/*

# 2) Create a global venv at /opt/venv and bootstrap pip
RUN python3.11 -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip setuptools wheel

# 3) Make that venv the default python/pip
ENV PATH="/opt/venv/bin:${PATH}"

# Install Azure CLI and Azure Functions Core Tools (Ubuntu 22.04)
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash \
    && curl https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -o packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends azure-functions-core-tools-4 \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# vscode user setup
RUN mkdir -p /home/vscode/.dotnet/tools \
    && mkdir -p /home/vscode/.local \
    && chown -R vscode:vscode /home/vscode/.dotnet /home/vscode/.local

# Switch to vscode user to install Poetry and .NET tools
USER vscode

# Configure PATH for vscode user
ENV PATH="${PATH}:/home/vscode/.dotnet/tools:/home/vscode/.local/bin"

# Install .NET global tools
RUN dotnet tool install -g dotnet-ef \
    && dotnet tool install -g Microsoft.dotnet-httprepl

# Install Poetry (as vscode user)
RUN curl -sSL https://install.python-poetry.org | python3 -

# Configure Poetry to use system Python (no separate virtualenv in Docker)
RUN poetry config virtualenvs.create false
