from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from services.groq_client import call_groq
from services.sanitiser import sanitise
import os
import json

report_bp = Blueprint("report", __name__)

REQUIRED_REPORT_KEYS = {
    "title",
    "executive_summary",
    "violation_overview",
    "risk_assessment",
    "recommendations",
    "conclusion"
}

FALLBACK_REPORT = {
    "title": "Regulatory Violation Compliance Report",
    "executive_summary": "A regulatory violation has been identified that requires immediate attention. This report outlines the violation details and recommended corrective actions.",
    "violation_overview": "The violation involves a breach of regulatory requirements. An internal review is recommended to determine the full scope of the violation.",
    "risk_assessment": "The violation poses financial, legal, and reputational risks to the organisation. Immediate corrective action is advised to minimise exposure.",
    "recommendations": [
        {
            "action_type": "Legal",
            "description": "Engage a regulatory compliance attorney to assess liability and prepare a response.",
            "priority": "High"
        },
        {
            "action_type": "Operational",
            "description": "Conduct an internal audit to identify root cause and implement corrective measures.",
            "priority": "High"
        },
        {
            "action_type": "Training",
            "description": "Provide mandatory compliance training to all relevant staff.",
            "priority": "Medium"
        }
    ],
    "conclusion": "Immediate action is required to address this violation and prevent recurrence. Please consult with your compliance team for next steps."
}

def load_prompt(filename: str, **kwargs) -> str:
    path = os.path.join("prompts", filename)
    with open(path, "r") as f:
        template = f.read()
    return template.format(**kwargs)

def validate_report(data) -> bool:
    if not isinstance(data, dict):
        return False
    return REQUIRED_REPORT_KEYS.issubset(data.keys())

@report_bp.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json()

    # Validate string fields
    string_fields = ["industry", "regulation_type", "violation_description", "severity"]
    for field in string_fields:
        if not data or not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    # Validate numeric fields
    for num_field in ["fine_min", "fine_max"]:
        if not data or data.get(num_field) is None:
            return jsonify({"error": f"{num_field} is required"}), 400
        try:
            float(data[num_field])
        except (ValueError, TypeError):
            return jsonify({"error": f"{num_field} must be a valid number"}), 400

    # Sanitise string inputs
    fields = {}
    for field in string_fields:
        cleaned, is_safe = sanitise(data[field])
        if not is_safe:
            return jsonify({"error": "Invalid input detected", "field": field}), 400
        fields[field] = cleaned

    # Load and fill prompt template
    prompt = load_prompt(
        "report.txt",
        industry=fields["industry"],
        regulation_type=fields["regulation_type"],
        violation_description=fields["violation_description"],
        severity=fields["severity"],
        fine_min=data["fine_min"],
        fine_max=data["fine_max"]
    )

    # Call Groq AI
    result = call_groq(prompt, temperature=0.3)

    # Parse and validate response
    if result is not None:
        try:
            cleaned = result.strip().replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
            if validate_report(parsed):
                return jsonify({
                    "report": parsed,
                    "is_fallback": False,
                    "generated_at": datetime.now(timezone.utc).isoformat()
                }), 200
        except (json.JSONDecodeError, Exception):
            pass

    # Return fallback if anything fails
    return jsonify({
        "report": FALLBACK_REPORT,
        "is_fallback": True,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }), 200