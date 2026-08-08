import json
import os

from flask import Flask, request, jsonify
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

app = Flask(__name__)

PUBLIC_KEY = os.environ.get("DISCORD_PUBLIC_KEY")


def verify_discord_request():
    if not PUBLIC_KEY:
        return False

    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp:
        return False

    try:
        body = request.get_data()

        verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

        verify_key.verify(
            timestamp.encode() + body,
            bytes.fromhex(signature)
        )

        return True

    except (BadSignatureError, ValueError, TypeError):
        return False


@app.route("/", methods=["GET", "POST"])
@app.route("/api/discord", methods=["GET", "POST"])
def discord_interactions():

    # GET is only for checking that the Vercel function is alive.
    if request.method == "GET":
        return jsonify({
            "status": "online",
            "service": "Discord Interactions"
        }), 200

    # Verify that the request actually came from Discord.
    if not verify_discord_request():
        return jsonify({
            "error": "Invalid Discord request"
        }), 401

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Invalid JSON"
            }), 400

        # Discord endpoint verification PING
        if data.get("type") == 1:
            return jsonify({
                "type": 1
            }), 200

        # Slash command
        if data.get("type") == 2:

            command_name = data.get("data", {}).get("name")

            if command_name == "ping":
                return jsonify({
                    "type": 4,
                    "data": {
                        "content": "🏓 Pong!"
                    }
                }), 200

            return jsonify({
                "type": 4,
                "data": {
                    "content": "Unknown command."
                }
            }), 200

        return jsonify({
            "type": 4,
            "data": {
                "content": "Unsupported interaction."
            }
        }), 200

    except Exception as e:
        print("ERROR:", repr(e))

        return jsonify({
            "error": "Internal server error"
        }), 500
