#!/usr/bin/env python3
"""define a _hash_password method that takes in a password string
    arguments and returns bytes
"""
import bcrypt

def _hash_password(password: str) -> bytes:
    """ hashes a pwd"""
    hashed_pwd = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_pwd.encode('utf-8')
