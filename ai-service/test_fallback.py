import requests

BASE_URL = "http://127.0.0.1:5000"

SAMPLE = {
    "industry": "Healthcare",
    "regulation_type": "HIPAA",
    "violation_description": "Unauthorized disclosure of patient records",
    "severity": "High",
    "fine_min": 100000,
    "fine_max": 500000
}

def test_fallback():
    print("\n🚀 Fallback Test\n")
    print("="*55)
    print("Testing /recommend fallback response...")
    print("="*55)

    resp = requests.post(
        f"{BASE_URL}/recommend",
        json={k: SAMPLE[k] for k in ["industry", "regulation_type",
                                      "violation_description", "severity"]}
    )
    data = resp.json()
    print(f"Status Code : {resp.status_code}")
    print(f"Is Fallback : {data.get('is_fallback')}")
    print(f"Has recommendations: {'recommendations' in data}")
    print(f"Recommendations count: {len(data.get('recommendations', []))}")

    print("\n" + "="*55)
    print("Testing /generate-report fallback response...")
    print("="*55)

    resp = requests.post(f"{BASE_URL}/generate-report", json=SAMPLE)
    data = resp.json()
    print(f"Status Code : {resp.status_code}")
    print(f"Is Fallback : {data.get('is_fallback')}")
    print(f"Has report  : {'report' in data}")

    print("\n✅ Fallback test complete!")

if __name__ == "__main__":
    test_fallback()