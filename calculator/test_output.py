import requests
import json

def test_endpoint(endpoint):
    print(f"\nTesting endpoint: {endpoint}")
    print("-" * 50)
    try:
        response = requests.get(f"http://127.0.0.1:8000{endpoint}")
        print("Status Code:", response.status_code)
        print("\nResponse Data:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print("Error:", str(e))

# Test all endpoints
print("Testing Average Calculator Microservice")
print("=" * 50)

# Test root endpoint
test_endpoint("/")

# Test all number endpoints
for number_type in ['e', 'p', 'f', 'r']:
    test_endpoint(f"/numbers/{number_type}") 