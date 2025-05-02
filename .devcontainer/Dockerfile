FROM mcr.microsoft.com/devcontainers/dotnet:6.0

# Install Python
ARG PYTHON_VERSION="3.10"
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python3-pip \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install Azure Functions Core Tools
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash \
    && apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends azure-functions-core-tools-4 \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install Python development tools
RUN pip3 install pylint black pytest fastapi uvicorn[standard] httpx

# Install .NET tools
RUN dotnet tool install -g dotnet-ef
RUN dotnet tool install -g Microsoft.dotnet-httprepl

# Set up a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Add dotnet tools to PATH
ENV PATH $PATH:/home/$USERNAME/.dotnet/tools

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME