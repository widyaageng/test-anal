#!/bin/bash

# Test script for Vector VRL parsing

echo "Testing Vector VRL parsing with sustxntotaldata.json"

# Check if vector binary exists in the container
if docker exec vector which vector > /dev/null 2>&1; then
    echo "✓ Vector binary found in container"
else
    echo "✗ Vector binary not found in container"
    echo "Installing vector in the container..."
    docker exec vector /bin/sh -c "curl --proto '=https' --tlsv1.2 -sSfL https://sh.vector.dev | bash -s -- -y --prefix /usr/local"
fi

# Copy the test config and data file to the container
echo "Copying test files to container..."
docker cp ./vectordotdev/test-vrl.yaml vector:/tmp/test-vrl.yaml
docker cp ./sustxntotaldata.json vector:/home/sustxntotaldata.json

# Run vector with the test configuration
echo "Running Vector test..."
echo "================================"
docker exec vector /usr/local/bin/vector --config /tmp/test-vrl.yaml --quiet

echo "================================"
echo "Test completed!"
