import requests
import time
import json

BASE_URL = "http://127.0.0.1:5000"

SAMPLE_DATA = {
    "industry": "Healthcare",
    "regulation_type": "HIPAA",
    "violation_description": "Patient records accessed without authorization by a third party vendor",
    "severity": "High",
    "fine_min": 50000,
    "fine_max": 250000
}

def print_result(endpoint, status_code, elapsed, is_fallback, result_preview):
    print("-" * 60)
    print(f"Endpoint     : {endpoint}")
    print(f"Status Code  : {status_code}")
    print(f"Response Time: {elapsed:.2f}s")
    print(f"Is Fallback  : {is_fallback}")
    print(f"Result       : {result_preview}")
    print("-" * 60)

def test_health():
    start = time.time()
    response = requests.get(f"{BASE_URL}/health")
    elapsed = time.time() - start
    data = response.json()
    result_preview = str(data.get("status", ""))[:80]
    is_fallback = data.get("is_fallback", "N/A")
    print_result("GET /health", response.status_code, elapsed, is_fallback, result_preview)

def test_describe():
    payload = {
        "industry": SAMPLE_DATA["industry"],
        "regulation_type": SAMPLE_DATA["regulation_type"],
        "violation_description": SAMPLE_DATA["violation_description"],
        "severity": SAMPLE_DATA["severity"]
    }
    start = time.time()
    response = requests.post(f"{BASE_URL}/describe", json=payload)
    elapsed = time.time() - start
    data = response.json()
    result_preview = str(data.get("result", ""))[:80]
    is_fallback = data.get("is_fallback", "N/A")
    print_result("POST /describe", response.status_code, elapsed, is_fallback, result_preview)

def test_recommend():
    payload = {
        "industry": SAMPLE_DATA["industry"],
        "regulation_type": SAMPLE_DATA["regulation_type"],
        "violation_description": SAMPLE_DATA["violation_description"],
        "severity": SAMPLE_DATA["severity"]
    }
    start = time.time()
    response = requests.post(f"{BASE_URL}/recommend", json=payload)
    elapsed = time.time() - start
    data = response.json()
    result_preview = str(data.get("recommendations", ""))[:80]
    is_fallback = data.get("is_fallback", "N/A")
    print_result("POST /recommend", response.status_code, elapsed, is_fallback, result_preview)

def test_generate_report():
    start = time.time()
    response = requests.post(f"{BASE_URL}/generate-report", json=SAMPLE_DATA)
    elapsed = time.time() - start
    data = response.json()
    result_preview = str(data.get("report", ""))[:80]
    is_fallback = data.get("is_fallback", "N/A")
    print_result("POST /generate-report", response.status_code, elapsed, is_fallback, result_preview)

if __name__ == "__main__":
    print("\n🚀 Running endpoint tests...\n")
    test_health()
    test_describe()
    test_recommend()
    test_generate_report()
    print("\n✅ All tests completed!")