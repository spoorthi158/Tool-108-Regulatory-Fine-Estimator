import os
import time
import logging
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("root")

def preload_model():
    try:
        logger.info("[STARTUP] Loading sentence-transformers model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        model.encode(["warm up"])
        logger.info("[STARTUP] sentence-transformers model loaded successfully!")
        return model
    except Exception as e:
        logger.error(f"[STARTUP] Failed to load sentence-transformers model: {e}")
        return None

embedding_model = preload_model()

def create_app():
    app = Flask(__name__)

    from routes.describe import describe_bp
    from routes.recommend import recommend_bp
    from routes.report import report_bp
    from routes.health import health_bp

    app.register_blueprint(describe_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(health_bp)

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = "default-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Server"] = "Tool-108"
        return response

    @app.before_request
    def start_timer():
        request._start_time = time.time()

    @app.after_request
    def log_timing(response):
        if hasattr(request, "_start_time"):
            elapsed = time.time() - request._start_time
            logger.info(f"[TIMING] {request.path} - {elapsed:.2f}s - {response.status_code}")
        return response

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return jsonify({
            "error": "Too many requests. Please slow down.",
            "retry_after_seconds": 60
        }), 429

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({"status": "ok", "service": "Tool-108 AI Service"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_ENV") == "development")