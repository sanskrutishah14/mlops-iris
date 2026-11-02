"""Send sample traffic to the API so Grafana has data to show.

Usage: python scripts/generate_traffic.py [count] [base_url]
"""
import json
import random
import sys
import time
import urllib.error
import urllib.request

COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 200
BASE = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000"

SAMPLES = [
    {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2},
    {"sepal_length": 6.0, "sepal_width": 2.9, "petal_length": 4.5, "petal_width": 1.5},
    {"sepal_length": 6.7, "sepal_width": 3.1, "petal_length": 5.6, "petal_width": 2.4},
]


def post(payload):
    req = urllib.request.Request(
        BASE + "/predict",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req).read()
    except urllib.error.HTTPError:
        pass  # expected for the deliberately bad requests


for i in range(COUNT):
    if i % 15 == 0:
        post({"sepal_length": "bad"})  # 422 error, shows up in the error panel
    else:
        post(random.choice(SAMPLES))
    time.sleep(0.05)
print(f"Sent {COUNT} requests to {BASE}")
