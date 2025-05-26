#!/bin/bash

# Set environment variables for testing
export TEST_FUNCTION_BASE_URL="http://localhost:7071"

# Run the tests
echo "Running Wallet Integration QA Tests..."
dotnet test

# Generate test report
echo "Generating test report..."
dotnet test --logger "trx;LogFileName=TestResults.trx"

echo "Tests completed. See TestResults.trx for detailed results."

