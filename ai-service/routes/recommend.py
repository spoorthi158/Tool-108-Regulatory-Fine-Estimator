from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from services.groq_client import call_groq
from services.sanitiser import sanitise
import os
import json

recommend_bp = Blueprint("recommend", __name__)

FALLBACK_RECOMMENDATIONS = [
    {
        "action_type": "Legal",
        "description": "Consult with a regulatory compliance attorney to assess liability and develop a response strategy.",
        "priority": "High"
    },
    {
        "action_type": "Operational",
        "description": "Conduct an internal audit to identify the root cause of the violation and implement corrective measures.",
        "priority": "High"
    },
    {
        "action_type": "Training",
        "description": "Provide mandatory compliance training to all relevant staff to prevent future violations.",
        "priority": "Medium"
    }
]

def load_prompt(filename: str, **kwargs) -> str:
    path = os.path.join("prompts", filename)
    with open(path, "r") as f:
        template = f.read()
    return template.format(**kwargs)

def validate_recommendations(data) -> bool:
    if not isinstance(data, list) or len(data) != 3:
        return False
    required_keys = {"action_type", "description", "priority"}
    for item in data:
        if not isinstance(item, dict):
            return False
        if not required_keys.issubset(item.keys()):
            return False
    return True

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    # Validate required fields
    required_fields = ["industry", "regulation_type", "violation_description", "severity"]
    for field in required_fields:
        if not data or not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    # Sanitise all inputs
    fields = {}
    for field in required_fields:
        cleaned, is_safe = sanitise(data[field])
        if not is_safe:
            return jsonify({"error": "Invalid input detected", "field": field}), 400
        fields[field] = cleaned

    # Load and fill prompt template
    prompt = load_prompt(
        "recommend.txt",
        industry=fields["industry"],
        regulation_type=fields["regulation_type"],
        violation_description=fields["violation_description"],
        severity=fields["severity"]
    )

    # Call Groq AI
    result = call_groq(prompt, temperature=0.3)

    # Parse and validate response
    if result is not None:
        try:
            cleaned = result.strip().replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)
            if validate_recommendations(parsed):
                return jsonify({
                    "recommendations": parsed,
                    "is_fallback": False,
                    "generated_at": datetime.now(timezone.utc).isoformat()
                }), 200
        except (json.JSONDecodeError, Exception):
            pass

    # Return fallback if Groq fails or JSON invalid
    return jsonify({
        "recommendations": FALLBACK_RECOMMENDATIONS,
        "is_fallback": True,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }), 200