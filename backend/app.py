from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# Local Imports
from routes.clients import clients_bp
from routes.health import health_bp
from routes.jobs import jobs_bp
from config import RATE_LIMIT

app = Flask(__name__)
CORS(app)  # allows requests from any origin — fine for local dev

# Limiter uses the caller's IP address as the key.
# Each unique IP gets its own counter.
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[RATE_LIMIT],
    headers_enabled=True  # adds X-RateLimit-* headers to every response
)

# Blueprints keep routes organized — each file owns its own endpoints
app.register_blueprint(clients_bp)
app.register_blueprint(health_bp)
app.register_blueprint(jobs_bp)


# Custom response when rate limit is exceeded
@app.errorhandler(429)
def rate_limit_handler(e):
    return jsonify({
        "error": "Too many requests",
        "message": str(e.description)
    }), 429

if __name__ == "__main__":
    app.run(debug=True, port=5000)