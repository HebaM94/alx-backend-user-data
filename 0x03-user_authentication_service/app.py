#!/usr/bin/env python3
"""Flask app
"""
from auth import Auth
from flask import Flask, abort, jsonify, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home() -> str:
    """ Home endpoint
        Return: Logout message JSON represented
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
