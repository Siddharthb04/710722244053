from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import httpx
import asyncio
from collections import deque
import random
import time

app = FastAPI(title="Average Calculator Microservice")

# Configuration
WINDOW_SIZE = 10
TIMEOUT_MS = 500

# Storage for different number types
number_storage: Dict[str, deque] = {
    'p': deque(maxlen=WINDOW_SIZE),  # prime numbers
    'f': deque(maxlen=WINDOW_SIZE),  # fibonacci numbers
    'e': deque(maxlen=WINDOW_SIZE),  # even numbers
    'r': deque(maxlen=WINDOW_SIZE),  # random numbers
}

class NumberResponse(BaseModel):
    windowPrevState: List[int]
    windowCurrState: List[int]
    numbers: List[int]
    avg: float

# Helper functions to generate numbers (simulating third-party server)
def generate_even_numbers(count=5):
    start = random.randint(1, 50) * 2
    return [start + i * 2 for i in range(count)]

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime_numbers(count=5):
    primes = []
    num = random.randint(2, 20)
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def generate_fibonacci_numbers(count=5):
    start = random.randint(0, 10)
    fib = [start, start + 1]
    while len(fib) < count:
        fib.append(fib[-1] + fib[-2])
    return fib[-count:]

def generate_random_numbers(count=5):
    return [random.randint(1, 100) for _ in range(count)]

async def get_numbers_from_generator(number_id: str) -> List[int]:
    # Simulate network delay (but keep it under timeout)
    await asyncio.sleep(random.uniform(0.1, 0.3))
    
    if number_id == 'e':
        return generate_even_numbers()
    elif number_id == 'p':
        return generate_prime_numbers()
    elif number_id == 'f':
        return generate_fibonacci_numbers()
    elif number_id == 'r':
        return generate_random_numbers()
    else:
        raise ValueError("Invalid number type")

@app.get("/numbers/{number_id}", response_model=NumberResponse)
async def get_numbers(number_id: str):
    if number_id not in ['p', 'f', 'e', 'r']:
        raise HTTPException(
            status_code=400,
            detail="Invalid number ID. Use 'p' for prime, 'f' for fibonacci, 'e' for even, or 'r' for random numbers"
        )
    
    # Store previous state
    prev_state = list(number_storage[number_id])
    
    try:
        # Get numbers from our generator (simulating third-party server)
        new_numbers = await asyncio.wait_for(
            get_numbers_from_generator(number_id),
            timeout=TIMEOUT_MS/1000
        )
        
        # Add new unique numbers
        for num in new_numbers:
            if num not in number_storage[number_id]:
                number_storage[number_id].append(num)
        
        curr_state = list(number_storage[number_id])
        avg = sum(curr_state) / len(curr_state) if curr_state else 0
        
        return NumberResponse(
            windowPrevState=prev_state,
            windowCurrState=curr_state,
            numbers=new_numbers,
            avg=round(avg, 2)
        )
            
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Request timeout - took longer than 500ms"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/")
async def root():
    return {
        "message": "Average Calculator Microservice",
        "endpoints": {
            "/numbers/e": "Get even numbers",
            "/numbers/p": "Get prime numbers",
            "/numbers/f": "Get fibonacci numbers",
            "/numbers/r": "Get random numbers"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Average Calculator Microservice...")
    print("Server running at http://localhost:8000")
    print("Available endpoints:")
    print("  - GET /numbers/e (even numbers)")
    print("  - GET /numbers/p (prime numbers)")
    print("  - GET /numbers/f (fibonacci numbers)")
    print("  - GET /numbers/r (random numbers)")
    uvicorn.run(app, host="127.0.0.1", port=8000) 