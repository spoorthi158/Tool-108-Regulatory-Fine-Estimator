import requests
import time

BASE_URL = "http://127.0.0.1:5000"

# 30 demo records covering all industries and severities
DEMO_RECORDS = [
    {"industry": "Healthcare", "regulation_type": "HIPAA", "violation_description": "Unauthorized disclosure of patient records to third party vendor", "severity": "High", "fine_min": 100000, "fine_max": 500000},
    {"industry": "Finance", "regulation_type": "AML", "violation_description": "Failure to file suspicious activity reports for transactions over $10,000", "severity": "High", "fine_min": 250000, "fine_max": 1000000},
    {"industry": "Technology", "regulation_type": "GDPR", "violation_description": "Customer data breach affecting 50,000 European users", "severity": "Critical", "fine_min": 500000, "fine_max": 2000000},
    {"industry": "Manufacturing", "regulation_type": "OSHA", "violation_description": "Failure to provide adequate safety equipment to workers", "severity": "Medium", "fine_min": 15000, "fine_max": 50000},
    {"industry": "Finance", "regulation_type": "SEC", "violation_description": "Insider trading based on non-public merger information", "severity": "Critical", "fine_min": 1000000, "fine_max": 5000000},
    {"industry": "Banking", "regulation_type": "SOX", "violation_description": "Inaccurate financial reporting in quarterly earnings statement", "severity": "High", "fine_min": 500000, "fine_max": 2000000},
    {"industry": "Retail", "regulation_type": "PCI DSS", "violation_description": "Unencrypted storage of customer credit card data", "severity": "High", "fine_min": 50000, "fine_max": 200000},
    {"industry": "Pharmaceutical", "regulation_type": "FDA", "violation_description": "Manufacturing facility failed GMP inspection with critical findings", "severity": "Critical", "fine_min": 1000000, "fine_max": 10000000},
    {"industry": "Technology", "regulation_type": "CCPA", "violation_description": "Failure to honor consumer data deletion requests within 45 days", "severity": "Medium", "fine_min": 25000, "fine_max": 75000},
    {"industry": "Finance", "regulation_type": "FINRA", "violation_description": "Broker made unsuitable investment recommendations to elderly clients", "severity": "High", "fine_min": 100000, "fine_max": 500000},
    {"industry": "Healthcare", "regulation_type": "HIPAA", "violation_description": "Lost laptop containing unencrypted patient records for 10,000 patients", "severity": "High", "fine_min": 200000, "fine_max": 800000},
    {"industry": "Banking", "regulation_type": "AML", "violation_description": "Inadequate KYC procedures allowing suspicious accounts to operate", "severity": "High", "fine_min": 500000, "fine_max": 2000000},
    {"industry": "Technology", "regulation_type": "GDPR", "violation_description": "Collecting personal data without explicit user consent", "severity": "Medium", "fine_min": 100000, "fine_max": 500000},
    {"industry": "Construction", "regulation_type": "OSHA", "violation_description": "Workers exposed to fall hazards without proper fall protection", "severity": "High", "fine_min": 50000, "fine_max": 165000},
    {"industry": "Finance", "regulation_type": "SEC", "violation_description": "Failure to disclose material information in IPO prospectus", "severity": "High", "fine_min": 500000, "fine_max": 3000000},
    {"industry": "Healthcare", "regulation_type": "HIPAA", "violation_description": "Employees accessing patient records without authorization", "severity": "Medium", "fine_min": 50000, "fine_max": 250000},
    {"industry": "Retail", "regulation_type": "PCI DSS", "violation_description": "Point of sale systems compromised by malware for 6 months", "severity": "Critical", "fine_min": 200000, "fine_max": 500000},
    {"industry": "Banking", "regulation_type": "SOX", "violation_description": "Material weakness in internal controls over financial reporting", "severity": "High", "fine_min": 250000, "fine_max": 1000000},
    {"industry": "Technology", "regulation_type": "GDPR", "violation_description": "Data processor failed to notify controller of breach within 72 hours", "severity": "Medium", "fine_min": 50000, "fine_max": 200000},
    {"industry": "Pharmaceutical", "regulation_type": "FDA", "violation_description": "Selling misbranded drugs without required labeling information", "severity": "High", "fine_min": 500000, "fine_max": 2000000},
    {"industry": "Finance", "regulation_type": "FINRA", "violation_description": "Failure to maintain required books and records for 3 years", "severity": "Medium", "fine_min": 25000, "fine_max": 100000},
    {"industry": "Healthcare", "regulation_type": "HIPAA", "violation_description": "Medical practice sent patient data to wrong recipients via email", "severity": "Low", "fine_min": 10000, "fine_max": 50000},
    {"industry": "Banking", "regulation_type": "AML", "violation_description": "Bank processed transactions for sanctioned entities unknowingly", "severity": "Critical", "fine_min": 1000000, "fine_max": 5000000},
    {"industry": "Technology", "regulation_type": "CCPA", "violation_description": "Company sold consumer data to third parties without disclosure", "severity": "High", "fine_min": 50000, "fine_max": 200000},
    {"industry": "Manufacturing", "regulation_type": "OSHA", "violation_description": "Chemical exposure levels exceeded permissible limits in facility", "severity": "High", "fine_min": 100000, "fine_max": 165000},
    {"industry": "Finance", "regulation_type": "SEC", "violation_description": "Ponzi scheme operated for 2 years defrauding 500 investors", "severity": "Critical", "fine_min": 5000000, "fine_max": 20000000},
    {"industry": "Retail", "regulation_type": "PCI DSS", "violation_description": "E-commerce site stored CVV codes in violation of PCI standards", "severity": "Medium", "fine_min": 10000, "fine_max": 50000},
    {"industry": "Banking", "regulation_type": "SOX", "violation_description": "CEO certified financial statements with known material errors", "severity": "Critical", "fine_min": 1000000, "fine_max": 5000000},
    {"industry": "Healthcare", "regulation_type": "HIPAA", "violation_description": "Business associate failed to sign BAA before accessing PHI", "severity": "Medium", "fine_min": 25000, "fine_max": 100000},
    {"industry": "Technology", "regulation_type": "GDPR", "violation_description": "Company transferred EU citizen data to non-adequate third country", "severity": "High", "fine_min": 200000, "fine_max": 1000000},
]

def test_record(index, record):
    print(f"\n{'='*60}")
    print(f"Record {index+1:02d} | {record['industry']} | {record['regulation_type']} | {record['severity']}")
    print(f"{'='*60}")

    # Test /describe
    start = time.time()
    resp = requests.post(f"{BASE_URL}/describe", json={
        "industry": record["industry"],
        "regulation_type": record["regulation_type"],
        "violation_description": record["violation_description"],
        "severity": record["severity"]
    })
    elapsed = time.time() - start
    data = resp.json()
    print(f"📋 /describe    → {resp.status_code} | {elapsed:.2f}s | fallback={data.get('is_fallback')}")
    print(f"   Preview: {str(data.get('result',''))[:100]}")

    # Test /recommend
    start = time.time()
    resp = requests.post(f"{BASE_URL}/recommend", json={
        "industry": record["industry"],
        "regulation_type": record["regulation_type"],
        "violation_description": record["violation_description"],
        "severity": record["severity"]
    })
    elapsed = time.time() - start
    data = resp.json()
    print(f"💡 /recommend   → {resp.status_code} | {elapsed:.2f}s | fallback={data.get('is_fallback')}")
    print(f"   Preview: {str(data.get('recommendations',''))[:100]}")

    # Test /generate-report
    start = time.time()
    resp = requests.post(f"{BASE_URL}/generate-report", json=record)
    elapsed = time.time() - start
    data = resp.json()
    print(f"📊 /report      → {resp.status_code} | {elapsed:.2f}s | fallback={data.get('is_fallback')}")
    print(f"   Preview: {str(data.get('report',''))[:100]}")

if __name__ == "__main__":
    print("🚀 Testing all 3 endpoints against 30 demo records...\n")
    print("⚠️  This will take several minutes due to AI calls.\n")

    passed = 0
    fallbacks = 0

    for i, record in enumerate(DEMO_RECORDS):
        try:
            test_record(i, record)
            passed += 1
        except Exception as e:
            print(f"❌ Record {i+1} failed: {e}")

    print(f"\n{'='*60}")
    print(f"✅ Completed: {passed}/30 records tested")
    print(f"{'='*60}")