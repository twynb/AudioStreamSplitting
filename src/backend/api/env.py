from flask import Blueprint, jsonify, request
from utils.env import get_env, set_env

env_bp = Blueprint("env", __name__)


@env_bp.route("/get", methods=["GET"])
def get():
    key = request.args.get("key")
    if not key:
        return jsonify({"error": "Key parameter missing"}), 400

    value = get_env(key)
    if value is None:
        return jsonify({"error": "Key not found"}), 404

    return jsonify({"value": value})


@env_bp.route("/set", methods=["POST"])
def set():
    data = request.json
    key = data.get("key")
    value = data.get("value")

    if not key or not value:
        return jsonify({"error": "Key and value are required"}), 400

    set_env(key, value)
    return "", 201
