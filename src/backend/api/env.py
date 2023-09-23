from flask import Blueprint, jsonify, request
from utils.env import set_env

env_bp = Blueprint("env", __name__)


@env_bp.route("/set", methods=["POST"])
def set():
    data = request.json
    key = data.get("key")
    value = data.get("value")

    if not key or not value:
        return jsonify({"error": "Key and value are required"}), 400

    set_env(key, value)
    return "", 201
