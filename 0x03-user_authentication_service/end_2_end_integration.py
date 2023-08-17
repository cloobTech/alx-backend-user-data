#!/usr/bin/env python3
""" End to End Integration Test """
import requests


BASE_URL = "http://localhost:5000"

def register_user(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200, "Registration failed"
    print("User registered successfully.")

def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401, "Login with wrong password should fail"
    print("Login with wrong password failed as expected.")

def log_in(email: str, password: str) -> str:
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200, "Login failed"
    session_id = response.cookies.get("session_id")
    assert session_id is not None, "Session ID not found in response"
    print("Logged in successfully.")
    return session_id

def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, "Profile access should be denied for unlogged user"
    print("Profile access denied for unlogged user as expected.")

def profile_logged(session_id: str) -> None:
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    assert response.status_code == 200, "Failed to access profile"
    print("Profile accessed successfully.")

def log_out(session_id: str) -> None:
    headers = {"Cookie": f"session_id={session_id}"}
    response = requests.delete(f"{BASE_URL}/sessions", headers=headers)
    assert response.status_code == 302, "Logout failed"
    print("Logged out successfully.")

def reset_password_token(email: str) -> str:
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, "Failed to get reset password token"
    reset_token = response.json().get("reset_token")
    assert reset_token is not None, "Reset token not found in response"
    print("Reset password token obtained successfully.")
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    data = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.put(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200, "Failed to update password"
    print("Password updated successfully.")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
