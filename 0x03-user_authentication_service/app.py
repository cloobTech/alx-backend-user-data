#!/usr/bin/env python3
"""
    A simple Api to help us with user authentication/registration
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def index():
    """
    Welcome route - index page of the app
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """Register a user"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = AUTH.register_user(email, password)
        return_val = {"email": f"{user.email}", "message": "user created"}
        return jsonify(return_val), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """Login a user"""
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        if not AUTH.valid_login(email, password):
            abort(401)
        else:
            session_id = AUTH.create_session(email)
            response = make_response(jsonify({"email": f"{email}",
                                             "message": "logged in"}))
            response.set_cookie("session_id", session_id)
            return response, 200
    except ValueError:
        return jsonify({"message": "Invalid Login"}), 401


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout a user"""
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/", code=302)
    except NoResultFound:
        return make_response(), 403
    return make_response(), 403


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """Get a user's profile"""
    try:
        session_id = request.cookies.get('session_id')
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    except NoResultFound:
        pass
    return make_response(), 403


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def reset_password():
    """ Reset a users password """
    try:
        email = request.form.get("email")
        reset_token = AUTH.get_reset_password_token(email=email)

        if reset_token:
            return jsonify({"email": f"{email}", "reset_token":
                            f"{reset_token}"}), 200
    except NoResultFound:
        pass
    return make_response(), 403


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password():
    """ update a user's password"""
    try:
        email = request.form.get("email")
        reset_token = request.form.get("reset_token")
        new_password = request.form.get("new_password")

        AUTH.update_password(reset_token, new_password)
        return jsonify({'email': f'{email}',
                        'message': 'password updated'}), 200
    except ValueError:
        return jsonify({'message': 'Invalid token'}), 403
    return make_response(), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=1)
