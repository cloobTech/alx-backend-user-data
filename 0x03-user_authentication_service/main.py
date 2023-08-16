#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from db import DB

db_in = DB()
email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))



user = db_in.find_user_by(email=email)
print(f'User - {user} | {user.session_id} | {user.hashed_password}')
