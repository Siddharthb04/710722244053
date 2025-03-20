import requests
import json

try:
    response = requests.get('http://127.0.0.1:8000/numbers/e')
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))
except requests.exceptions.ConnectionError:
    print("Connection Error: Could not connect to the server")
except Exception as e:
    print("Error:", str(e)) 