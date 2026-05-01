from flask import Blueprint, jsonify
from datetime import datetime, timezone
import time
import os
import redis

health_bp = Blueprint("health", __name__)

START_TIME = time.time()

def get_redis_client():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )

@health_bp.route("/health", methods=["GET"])
def health():
    uptime_seconds = int(time.time() - START_TIME)

    # Check Redis connection
    redis_connected = False
    try:
        r = get_redis_client()
        r.ping()
        redis_connected = True
    except Exception:
        redis_connected = False

    return jsonify({
        "status": "ok",
        "model": "llama-3.3-70b-versatile",
        "version": "1.0.0",
        "uptime_seconds": uptime_seconds,
        "redis_connected": redis_connected,
        "endpoints": [
            {"path": "/describe", "method": "POST"},
            {"path": "/recommend", "method": "POST"},
            {"path": "/generate-report", "method": "POST"},
            {"path": "/health", "method": "GET"}
        ],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200