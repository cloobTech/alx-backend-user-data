from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route("/")
def welcome():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        user = AUTH.register_user(email, password)
        return_val = {"email": f"{user.email}", "message": "user created"}
        return jsonify(return_val), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
