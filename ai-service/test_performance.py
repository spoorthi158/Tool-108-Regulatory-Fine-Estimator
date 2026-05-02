import requests
import time

BASE_URL = "http://127.0.0.1:5000"

SAMPLE = {
    "industry": "Healthcare",
    "regulation_type": "HIPAA",
    "violation_description": "Unauthorized disclosure of patient records",
    "severity": "High",
    "fine_min": 100000,
    "fine_max": 500000
}

def test_endpoint_speed(name, method, url, payload=None):
    times = []
    print(f"\n{'='*55}")
    print(f"Testing: {name}")
    print(f"{'='*55}")
    for i in range(3):
        start = time.time()
        if method == "GET":
            resp = requests.get(url)
        else:
            resp = requests.post(url, json=payload)
        elapsed = time.time() - start
        times.append(elapsed)
        fallback = resp.json().get("is_fallback", "N/A")
        print(f"  Run {i+1}: {elapsed:.2f}s | status={resp.status_code} | fallback={fallback}")
    avg = sum(times) / len(times)
    print(f"  Average: {avg:.2f}s")
    if avg < 3:
        print(f"  ✅ PASS — under 3 seconds average")
    else:
        print(f"  ⚠️  SLOW — over 3 seconds average")
    return avg

def test_cache(name, url, payload):
    print(f"\n{'='*55}")
    print(f"Cache Test: {name}")
    print(f"{'='*55}")
    
    # First request
    start = time.time()
    requests.post(url, json=payload)
    first = time.time() - start
    print(f"  First request:  {first:.2f}s (no cache)")
    
    # Second request (should be faster if cached)
    start = time.time()
    requests.post(url, json=payload)
    second = time.time() - start
    print(f"  Second request: {second:.2f}s (cached if Redis running)")
    
    if second < first:
        print(f"  ✅ Cache working — second request faster!")
    else:
        print(f"  ℹ️  Redis not running locally — cache will work in Docker")

if __name__ == "__main__":
    print("🚀 Performance & Cache Test\n")

    # Test 1 - Speed tests
    test_endpoint_speed(
        "POST /describe",
        "POST",
        f"{BASE_URL}/describe",
        {k: SAMPLE[k] for k in ["industry", "regulation_type", "violation_description", "severity"]}
    )

    test_endpoint_speed(
        "POST /recommend",
        "POST",
        f"{BASE_URL}/recommend",
        {k: SAMPLE[k] for k in ["industry", "regulation_type", "violation_description", "severity"]}
    )

    test_endpoint_speed(
        "POST /generate-report",
        "POST",
        f"{BASE_URL}/generate-report",
        SAMPLE
    )

    # Test 2 - Cache tests
    test_cache(
        "/describe cache",
        f"{BASE_URL}/describe",
        {k: SAMPLE[k] for k in ["industry", "regulation_type", "violation_description", "severity"]}
    )

    print(f"\n{'='*55}")
    print("✅ Performance tests complete!")
    print(f"{'='*55}")