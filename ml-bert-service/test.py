import requests
import json

URL = "http://localhost:8000/predict"
payload = {
    "text": "Looking for a senior backend developer with Node.js, AWS, microservices, experience in architecture design and team leadership.",
    "top_k": 5
}

resp = requests.post(URL, json=payload)
print("Status:", resp.status_code)
print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
