from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from services.groq_client import call_groq
from services.sanitiser import sanitise
import os

describe_bp = Blueprint("describe", __name__)

def load_prompt(filename: str, **kwargs) -> str:
    path = os.path.join("prompts", filename)
    with open(path, "r") as f:
        template = f.read()
    return template.format(**kwargs)

@describe_bp.route("/describe", methods=["POST"])
def describe():
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
        "describe.txt",
        industry=fields["industry"],
        regulation_type=fields["regulation_type"],
        violation_description=fields["violation_description"],
        severity=fields["severity"]
    )

    # Call Groq AI
    result = call_groq(prompt, temperature=0.3)
    if result is None:
        return jsonify({
            "error": "AI service unavailable",
            "is_fallback": True
        }), 503

    return jsonify({
        "result": result,
        "is_fallback": False,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }), 200