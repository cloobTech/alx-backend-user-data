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

print(auth.get_reset_password_token(email))
print(auth.create_session("unknown@email.com"))



