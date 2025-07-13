import os
import requests
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

@app.post('/trigger-webhook')
def trigger_webhook():
    if not WEBHOOK_URL:
        return jsonify(success=False, error="WEBHOOK_URL not configured"), 500
    try:
        resp = requests.post(WEBHOOK_URL, json={"message": "trigger"})
        resp.raise_for_status()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
