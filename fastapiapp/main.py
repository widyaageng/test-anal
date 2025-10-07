from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Gauge
import asyncio
import time
import random

# Create FastAPI app
app = FastAPI(title="FastAPI Metrics Demo", version="1.0.0")

# Initialize Prometheus instrumentator
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Custom Prometheus metrics
random_counter = Counter(
    'sus_transactions', 
    'Count of random values generated to mimic sus transactions', 
    ['category', 'component']  # labels: 'low' for < 0.1, 'high' for >= 0.1
)

random_latency_gauge = Gauge(
    'upstream_call_latency', 
    'Latency of random number generation and processing mimicking upstream calls latency',
    ['component']
)

@app.get("/")
async def root():
    """Root endpoint"""
    start_time = time.time()
    await asyncio.sleep(random.uniform(0.1, 0.2))
    total_latency = time.time() - start_time
    if random.random() < 0.1:
        random_counter.labels(category='low', component='/').inc()
    else:
        random_counter.labels(category='high', component='/').inc()
    random_latency_gauge.labels('/').set(total_latency)

    return {"message": "Hello World from FastAPI with Prometheus metrics!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    start_time = time.time()
    await asyncio.sleep(random.uniform(0.1, 0.2))
    total_latency = time.time() - start_time
    
    if random.random() < 0.1:
        random_counter.labels(category='low', component='/health').inc()
    else:
        random_counter.labels(category='high', component='/health').inc()
    random_latency_gauge.labels('/health').set(total_latency)
    
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/slow")
async def slow_endpoint():
    """Slow endpoint to demonstrate latency metrics"""
    start_time = time.time()
    
    # Simulate some processing time
    sleep_duration = random.uniform(0.1, 2.0)
    await asyncio.sleep(sleep_duration)
    
    # Add metrics
    if random.random() < 0.1:
        random_counter.labels(category='low', component='/slow').inc()
    else:
        random_counter.labels(category='high', component='/slow').inc()
    
    total_latency = time.time() - start_time
    random_latency_gauge.labels('/slow').set(total_latency)
    
    return {"message": "This was a slow operation", "duration": sleep_duration}

@app.get("/error")
async def error_endpoint():
    """Endpoint that sometimes fails to demonstrate error metrics"""
    start_time = time.time()
    await asyncio.sleep(random.uniform(0.1, 0.2))
    
    # Add metrics
    if random.random() < 0.1:
        random_counter.labels(category='low', component='/error').inc()
    else:
        random_counter.labels(category='high', component='/error').inc()
    
    total_latency = time.time() - start_time
    random_latency_gauge.labels('/error').set(total_latency)
    
    if random.random() < 0.3:  # 30% chance of error
        raise HTTPException(status_code=500, detail="Random server error")
    return {"message": "Success!"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Parameterized endpoint to demonstrate path metrics"""
    start_time = time.time()
    await asyncio.sleep(random.uniform(0.1, 0.2))
    
    # Add metrics
    if random.random() < 0.1:
        random_counter.labels(category='low', component='/users').inc()
    else:
        random_counter.labels(category='high', component='/users').inc()
    
    total_latency = time.time() - start_time
    random_latency_gauge.labels('/users').set(total_latency)
    
    return {"user_id": user_id, "name": f"User {user_id}", "active": True}

@app.get("/business")
async def business_wrapped_with_random_metrics_endpoint():
    """Endpoint to demonstrate custom metrics with random value generation"""
    start_time = time.time()
    
    # Generate random value
    random_value = random.random()
    
    # Add random sleep between 0.1-0.3 seconds
    sleep_duration = random.uniform(0.1, 0.3)
    await asyncio.sleep(sleep_duration)
    
    # Update counter based on random value
    if random_value < 0.1:
        random_counter.labels(category='low', component='/business').inc()
        category = 'low'
    else:
        random_counter.labels(category='high', component='/business').inc()
        category = 'high'
    
    # Calculate and update latency gauge
    total_latency = time.time() - start_time
    random_latency_gauge.labels('/business').set(total_latency)
    
    return {
        "random_value": random_value,
        "category": category,
        "sleep_duration": sleep_duration,
        "total_latency": total_latency,
        "message": f"Random value {random_value:.4f} categorized as '{category}'"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
