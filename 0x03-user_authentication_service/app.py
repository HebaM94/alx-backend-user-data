#!/usr/bin/env python3
"""Flask app
"""
from auth import Auth
from flask import Flask, abort, jsonify, request, redirect, url_for

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home() -> str:
    """ Home endpoint
        Return: Logout message JSON represented
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def user() -> str:
    """ Register user endpoint
        Return: User created message JSON represented
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """ Login
        Return: Session ID JSON represented
    """
    email = request.form.get("email")
    password = request.form.get("password")
    user_id = AUTH.valid_login(email, password)
    if not user_id:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
