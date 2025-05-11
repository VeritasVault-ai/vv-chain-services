# Tests

This directory contains tests for the VeritasVault project.

## Structure

The test directory is organized to mirror the main project structure:

- `function-apps/` - Tests for Azure Functions
- `ml-engine/` - Tests for the ML Engine
- `integration/` - Integration tests across components

## Running Tests

### Unit Tests

Unit tests can be run using the appropriate test runner for each component:

- For .NET: `dotnet test`
- For Python: `pytest`

### Integration Tests

Integration tests may require additional setup and can be run using the scripts in the `integration` directory.

## Test Guidelines

1. All new features should include tests
2. Aim for high test coverage
3. Tests should be independent and idempotent
4. Use appropriate mocking for external dependencies
