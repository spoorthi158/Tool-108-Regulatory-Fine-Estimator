import os

def load_prompt(filename: str, **kwargs) -> str:
    path = os.path.join("prompts", filename)
    with open(path, "r") as f:
        template = f.read()
    return template.format(**kwargs)

def test_describe_prompt():
    result = load_prompt(
        "describe.txt",
        industry="Healthcare",
        regulation_type="HIPAA",
        violation_description="Unauthorized disclosure of patient records",
        severity="High"
    )
    assert "{industry}" not in result
    assert "{regulation_type}" not in result
    assert "{violation_description}" not in result
    assert "{severity}" not in result
    assert "Healthcare" in result
    assert "HIPAA" in result
    print("✅ describe.txt — PASSED")

def test_recommend_prompt():
    result = load_prompt(
        "recommend.txt",
        industry="Finance",
        regulation_type="AML",
        violation_description="Failure to report suspicious transactions",
        severity="Medium"
    )
    assert "{industry}" not in result
    assert "{regulation_type}" not in result
    assert "{violation_description}" not in result
    assert "{severity}" not in result
    assert "Finance" in result
    assert "AML" in result
    print("✅ recommend.txt — PASSED")

def test_report_prompt():
    result = load_prompt(
        "report.txt",
        industry="Banking",
        regulation_type="GDPR",
        violation_description="Customer data breach affecting 10,000 records",
        severity="Critical",
        fine_min=100000,
        fine_max=500000
    )
    assert "{industry}" not in result
    assert "{regulation_type}" not in result
    assert "{violation_description}" not in result
    assert "{severity}" not in result
    assert "{fine_min}" not in result
    assert "{fine_max}" not in result
    assert "Banking" in result
    assert "GDPR" in result
    print("✅ report.txt — PASSED")

if __name__ == "__main__":
    print("Running prompt template tests...\n")
    test_describe_prompt()
    test_recommend_prompt()
    test_report_prompt()
    print("\n✅ All prompt templates loaded and filled correctly!")