from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from routes.clients import clients_bp
from routes.health  import health_bp
from routes.jobs    import jobs_bp
from config         import RATE_LIMIT
from scheduler      import start as start_scheduler
from logger         import get_logger

logger = get_logger(__name__)
app    = Flask(__name__)
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[RATE_LIMIT],
    headers_enabled=True
)

app.register_blueprint(clients_bp)
app.register_blueprint(health_bp)
app.register_blueprint(jobs_bp)

@app.errorhandler(429)
def rate_limit_handler(e):
    return jsonify({"error": "Too many requests"}), 429

# Start the background scheduler when Flask starts
# use_reloader=False prevents the scheduler from starting twice in debug mode
if __name__ == "__main__":
    start_scheduler()
    logger.info("Flask starting on port 5000")
    app.run(debug=True, port=5000, use_reloader=False)