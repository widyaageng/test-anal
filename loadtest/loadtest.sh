#!/bin/bash

# Configuration
BASE_URL="http://fastapi-app:8000"
# Array of all available endpoints
ENDPOINTS=(
    "/"
    "/health"
    "/slow"
    "/error"
    "/users/1"
    "/users/42"
    "/users/999"
    "/business"
)

RPS=1  # Requests per second
DURATION=86400  # Run for 24 hours (in seconds), effectively forever for testing

echo "Starting round-robin load test against $BASE_URL"
echo "Endpoints: ${ENDPOINTS[@]}"
echo "Rate: $RPS requests per second"
echo "Duration: Running continuously (will restart if ab finishes)"

# Function to run round-robin load test
run_load_test() {
    local endpoint_index=0
    local num_endpoints=${#ENDPOINTS[@]}
    local sleep_time=$(echo "scale=2; 1 / $RPS" | bc -l)
    
    echo "Running round-robin across $num_endpoints endpoints"
    echo "Sleep time between requests: $sleep_time seconds"
    
    while true; do
        # Get current endpoint
        local current_endpoint="${ENDPOINTS[$endpoint_index]}"
        local full_url="$BASE_URL$current_endpoint"
        
        echo "$(date): Testing endpoint [$((endpoint_index + 1))/$num_endpoints]: $current_endpoint"
        
        # Run single request to current endpoint
        local ab_output=$(ab -n 1 -c 1 -q "$full_url" 2>&1)
        
        # Check if ab command was successful
        if [ $? -eq 0 ]; then
            echo "$(date): Request to $current_endpoint completed successfully"
        else
            echo "$(date): Warning - Request to $current_endpoint failed: $ab_output"
        fi
        
        # Move to next endpoint (round-robin)
        endpoint_index=$(( (endpoint_index + 1) % num_endpoints ))
        
        # Wait to maintain RPS
        sleep $sleep_time
    done
}

# Wait for the FastAPI service to be ready
echo "Waiting for FastAPI service to be ready..."
while ! curl -s "$BASE_URL/health" > /dev/null; do
    echo "$(date): FastAPI not ready yet, waiting 5 seconds..."
    sleep 5
done

echo "$(date): FastAPI service is ready, starting round-robin load test..."

# Install bc for floating point calculations
apk add --no-cache bc > /dev/null 2>&1

# Start the continuous load test
run_load_test
