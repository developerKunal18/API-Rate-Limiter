from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Store request history
request_log = {}

# Configuration
RATE_LIMIT = 5      # requests
TIME_WINDOW = 60    # seconds

# ---------- Middleware ----------
@app.before_request
def rate_limiter():
    client_ip = request.remote_addr

    current_time = time.time()

    if client_ip not in request_log:
        request_log[client_ip] = []

    # Remove old requests
    request_log[client_ip] = [
        timestamp
        for timestamp in request_log[client_ip]
        if current_time - timestamp < TIME_WINDOW
    ]

    # Check limit
    if len(request_log[client_ip]) >= RATE_LIMIT:
        return jsonify({
            "message": "Rate limit exceeded"
        }), 429

    request_log[client_ip].append(current_time)

# ---------- Test API ----------
@app.route("/")
def home():
    return jsonify({
        "message": "API is working"
    })

# ---------- User API ----------
@app.route("/users")
def users():
    return jsonify([
        {"id": 1, "name": "Rahul"},
        {"id": 2, "name": "Amit"}
    ])

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
