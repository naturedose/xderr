import os
import json

from flask import Flask, request, jsonify
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

app = Flask(__name__)

PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")


@app.route("/api/discord", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "service": "Discord Interactions"
    })


@app.route("/api/discord", methods=["POST"])
def discord_interaction():

    if not PUBLIC_KEY:
        return jsonify({
            "error": "DISCORD_PUBLIC_KEY is missing"
        }), 500

    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp:
        return jsonify({
            "error": "Missing Discord signature headers"
        }), 401

    body = request.get_data()

    try:
        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

        verify_key.verify(
            timestamp.encode() + body,
            bytes.fromhex(signature)
        )

    except (BadSignatureError, ValueError, TypeError):
        print("Discord signature verification failed")
        return jsonify({
            "error": "Invalid signature"
        }), 401

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    # Discord PING verification
    if data.get("type") == 1:
        print("Discord PING received")
        return jsonify({
            "type": 1
        })

    # Slash command
    if data.get("type") == 2:

        command = data.get("data", {}).get("name")

        if command == "ping":
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
