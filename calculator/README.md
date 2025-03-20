# Average Calculator Microservice

This microservice calculates averages for different types of numbers (prime, fibonacci, even, and random) fetched from a third-party server.

## Features

- REST API endpoint `/numbers/{numberid}` that accepts qualified number IDs
- Supported number IDs: 
  - 'p' for prime numbers
  - 'f' for fibonacci numbers
  - 'e' for even numbers
  - 'r' for random numbers
- Configurable window size (default: 10)
- Automatic handling of duplicates
- 500ms timeout for third-party server requests
- Maintains window state and provides averages

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the service:
   - Update TEST_SERVER_URL in main.py with your third-party server URL
   - Adjust WINDOW_SIZE if needed (default: 10)

3. Run the service:
```bash
python main.py
```

The service will start on http://localhost:8000

## API Usage

### GET /numbers/{numberid}

Example request:
```bash
curl http://localhost:8000/numbers/p
```

Example response:
```json
{
    "windowPrevState": [2, 3, 5, 7],
    "windowCurrState": [2, 3, 5, 7, 11],
    "numbers": [11],
    "avg": 5.60
}
```

### Response Format
- windowPrevState: Numbers in the window before the current request
- windowCurrState: Numbers in the window after the current request
- numbers: New numbers received from the third-party server
- avg: Average of numbers in the current window

### Error Responses
- 400: Invalid number ID
- 502: Test server error
- 504: Request timeout (>500ms)
- 500: Internal server error 