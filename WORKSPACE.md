# VeritasVault Risk Bot Workspace Guide

This document provides detailed information about the VS Code workspace configuration for the VeritasVault Risk Bot project and how to use it effectively.

## Table of Contents

- [Workspace Overview](#workspace-overview)
- [Workspace Structure](#workspace-structure)
- [Development Tools](#development-tools)
- [Tasks](#tasks)
- [Debugging](#debugging)
- [Extensions](#extensions)
- [Settings](#settings)
- [Customizing Your Workspace](#customizing-your-workspace)
- [Troubleshooting](#troubleshooting)

## Workspace Overview

The VeritasVault Risk Bot project uses a VS Code workspace configuration to organize the different components of the system and provide a consistent development experience. The workspace is designed to work with Dev Containers, ensuring all developers have the same environment regardless of their local setup.

## Workspace Structure

The workspace is organized into the following folders:

```
vv-chain-services/
├── Root                    # Root folder containing all project files
├── Azure Functions         # .NET Azure Functions (function-apps directory)
├── ML Engine              # Python ML Engine (src/ml-engine directory)
└── Tests                  # Test directories (tests directory)
```

This structure allows you to:
- Navigate between different parts of the project easily
- Focus on specific components when needed
- Run commands and tasks in the appropriate context

## Development Tools

The workspace is configured to work with:

- **Azure Functions**: Tools for developing and debugging Azure Functions
- **Python**: Tools for developing and debugging the ML Engine
- **Docker**: Container management for local development
- **Git**: Source control integration

## Tasks

The workspace includes several predefined tasks to streamline development. You can access these by pressing `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) and typing "Tasks: Run Task".

### Available Tasks

| Task Name | Description |
|-----------|-------------|
| Start ML-Engine | Starts the Python FastAPI service on port 8000 |
| Start Azure Function | Starts the .NET Azure Function locally |
| Start Full Stack | Starts both the ML-Engine and Azure Function in parallel |
| Run .NET Tests | Runs the test suite for the Azure Functions |
| Run Python Tests | Runs the test suite for the ML Engine |
| Run All Tests | Runs both test suites sequentially |

### Running Tasks

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
2. Type "Tasks: Run Task" and select it
3. Choose the task you want to run from the list

You can also configure keyboard shortcuts for frequently used tasks in VS Code's keyboard shortcuts settings.

## Debugging

The workspace includes launch configurations for debugging both the Azure Functions and the ML Engine.

### Available Debug Configurations

| Configuration | Description |
|---------------|-------------|
| Attach to .NET Functions | Attaches the debugger to a running Azure Functions process |
| Python: FastAPI | Launches the ML Engine with the debugger attached |
| Python: Current File | Runs the currently open Python file with the debugger |
| Run Full Stack | Compound configuration that launches both services |

### Starting a Debug Session

1. Open the Debug panel in VS Code (Ctrl+Shift+D or Cmd+Shift+D on macOS)
2. Select the configuration you want to use from the dropdown
3. Click the green play button or press F5

### Debug Features

- Set breakpoints by clicking in the gutter next to line numbers
- Inspect variables in the Variables panel during debugging
- Use the Debug Console to evaluate expressions
- Step through code using the debug toolbar

## Extensions

The workspace recommends several extensions to enhance your development experience. When you open the workspace for the first time, VS Code will prompt you to install these extensions.

### Key Extensions

#### .NET Development
- C# (ms-dotnettools.csharp)
- C# Dev Kit (ms-dotnettools.csdevkit)
- .NET Test Explorer (formulahendry.dotnet-test-explorer)
- Azure Functions (ms-azuretools.vscode-azurefunctions)

#### Python Development
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Black Formatter (ms-python.black-formatter)
- Python Docstring Generator (njpwerner.autodocstring)
- MyPy Type Checker (matangover.mypy)

#### Cloud & DevOps
- Docker (ms-azuretools.vscode-docker)
- Kubernetes (ms-kubernetes-tools.vscode-kubernetes-tools)
- Azure Account (ms-vscode.azure-account)

#### General Development
- GitHub Copilot (github.copilot)
- GitLens (eamodio.gitlens)
- YAML (redhat.vscode-yaml)
- Prettier (esbenp.prettier-vscode)
- EditorConfig (editorconfig.editorconfig)

#### Quality & Testing
- Code Spell Checker (streetsidesoftware.code-spell-checker)
- IntelliCode (visualstudioexptteam.vscodeintellicode)
- Coverage Gutters (ryanluker.vscode-coverage-gutters)
- Markdown All in One (yzhang.markdown-all-in-one)

#### Productivity
- Todo Tree (gruntfuggly.todo-tree)
- Better Comments (aaron-bond.better-comments)
- Path Intellisense (christian-kohler.path-intellisense)
- Error Lens (usernamehw.errorlens)

## Settings

The workspace includes preconfigured settings for:

- Code formatting
- Linting
- File exclusions
- Language-specific settings
- Editor preferences

### Key Settings

#### C# Settings
- Default formatter: ms-dotnettools.csharp
- Format on save: enabled
- Organize imports on save: enabled

#### Python Settings
- Default formatter: Black
- Format on save: enabled
- Organize imports on save: enabled
- Line length: 88 characters (Black default)

#### Editor Settings
- Rulers at 88 and 120 characters
- File exclusions for common build artifacts and temporary files
- Spell checking with common technical terms added to the dictionary

## Customizing Your Workspace

You can customize the workspace to better suit your preferences:

### Personal Settings

To add personal settings that won't affect other team members:

1. Create a `.vscode/settings.json` file in your local copy of the repository
 (this file is gitignored)
2. Add your personal settings to this file

### Additional Tasks

To add custom tasks:

1. Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P` on macOS)
2. Type "Tasks: Configure Task" and select it
3. Choose "Create tasks.json file from template"
4. Add your custom tasks to the file

## Troubleshooting

### Common Issues

#### Dev Container Not Building
- Ensure Docker Desktop is running
- Check that you have sufficient disk space
- Try rebuilding the container: Command Palette > "Remote-Containers: Rebuild Container"

#### Azure Functions Not Starting
- Check that the Azure Functions Core Tools are installed in the container
- Verify that `local.settings.json` exists in the function-apps directory
- Check for port conflicts (default port is 7071)

#### ML Engine Not Starting
- Ensure all Python dependencies are installed: `pip install -r requirements.txt`
- Check for port conflicts (default port is 8000)
- Verify that the Python path is correctly set in VS Code

#### Debugging Not Working
- For .NET: Ensure the Azure Functions host is running
- For Python: Check that the Python extension is correctly configured
- Verify that the correct debug configuration is selected

### Getting Help

If you encounter issues not covered here:

1. Check the project's GitHub issues to see if the problem has been reported
2. Consult the documentation for the specific tool or extension you're having trouble with
3. Ask for help in the project's communication channels
4. Create a new issue with detailed information about the problem

## Additional Resources

- [VS Code Documentation](https://code.visualstudio.com/docs)
- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Dev Containers Documentation](https://code.visualstudio.com/docs/remote/containers)