from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import random
from collections import deque

app = FastAPI()

# Configuration
WINDOW_SIZE = 10

# Storage for numbers
windows = {
    'e': deque(maxlen=WINDOW_SIZE),  # even numbers
    'p': deque(maxlen=WINDOW_SIZE),  # prime numbers
    'f': deque(maxlen=WINDOW_SIZE),  # fibonacci numbers
    'r': deque(maxlen=WINDOW_SIZE),  # random numbers
}

class Response(BaseModel):
    windowPrevState: List[int]
    windowCurrState: List[int]
    numbers: List[int]
    avg: float

def generate_numbers(type_id: str, count: int = 5) -> List[int]:
    if type_id == 'e':  # Even numbers
        start = random.randint(1, 10) * 2
        return [start + i * 2 for i in range(count)]
    
    elif type_id == 'p':  # Prime numbers
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        return random.sample(primes, min(count, len(primes)))
    
    elif type_id == 'f':  # Fibonacci numbers
        fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        return random.sample(fib, min(count, len(fib)))
    
    else:  # Random numbers
        return [random.randint(1, 100) for _ in range(count)]

@app.get("/numbers/{type_id}")
async def get_numbers(type_id: str):
    if type_id not in ['e', 'p', 'f', 'r']:
        raise HTTPException(
            status_code=400,
            detail="Invalid type. Use 'e' for even, 'p' for prime, 'f' for fibonacci, or 'r' for random"
        )
    
    # Store previous state
    prev_state = list(windows[type_id])
    
    # Generate new numbers
    new_numbers = generate_numbers(type_id)
    
    # Add new unique numbers
    for num in new_numbers:
        if num not in windows[type_id]:
            windows[type_id].append(num)
    
    # Get current state
    curr_state = list(windows[type_id])
    
    # Calculate average
    avg = sum(curr_state) / len(curr_state) if curr_state else 0
    
    return Response(
        windowPrevState=prev_state,
        windowCurrState=curr_state,
        numbers=new_numbers,
        avg=round(avg, 2)
    )

@app.get("/")
async def root():
    return {
        "message": "Average Calculator API",
        "endpoints": {
            "/numbers/e": "Get even numbers",
            "/numbers/p": "Get prime numbers",
            "/numbers/f": "Get fibonacci numbers",
            "/numbers/r": "Get random numbers"
        }
    }

if __name__ == "__main__":
    print("\n=== Average Calculator API ===")
    print("Server is starting...")
    print("Once running, you can access:")
    print("1. http://localhost:8000/numbers/e - for even numbers")
    print("2. http://localhost:8000/numbers/p - for prime numbers")
    print("3. http://localhost:8000/numbers/f - for fibonacci numbers")
    print("4. http://localhost:8000/numbers/r - for random numbers\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000) 