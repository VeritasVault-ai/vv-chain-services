# Azure Functions

This directory contains Azure Functions for the VeritasVault project.

## Getting Started

To develop Azure Functions:

1. Make sure you have the [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local) installed
2. Use the VS Code Azure Functions extension to create new functions
3. Test functions locally before deploying to Azure

## Project Structure

- `src/` - Contains the source code for Azure Functions
- `bin/` - Contains compiled output (generated during build)
- `obj/` - Contains intermediate build files

## Deployment

Functions are deployed to Azure using the Azure Functions extension or Azure DevOps pipelines.