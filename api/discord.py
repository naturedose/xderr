import json
import os

from flask import Flask, request, jsonify
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

app = Flask(__name__)

PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]


@app.route("/", methods=["POST"])
def discord_interactions():
    body = request.get_data()

    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp:
        return jsonify({"error": "Missing Discord signature headers"}), 401

    try:
        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
        verify_key.verify(
            timestamp.encode() + body,
            bytes.fromhex(signature)
        )
    except (BadSignatureError, ValueError):
        return jsonify({"error": "Invalid request signature"}), 401

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400

    # Discord endpoint verification
    if data.get("type") == 1:
        return jsonify({"type": 1})

    # Slash command
    if data.get("type") == 2:
        command_name = data.get("data", {}).get("name")

        if command_name == "ping":
            return jsonify({
                "type": 4,
                "data": {
                    "content": "🏓 Pong!"
                }
            })

        return jsonify({
            "type": 4,
            "data": {
                "content": "Unknown command."
            }
        })

    return jsonify({
        "type": 4,
        "data": {
            "content": "Unsupported interaction."
        }
    })
