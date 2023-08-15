import bcrypt

def generate_salt_and_hash(password: str) -> bytes:
    hashed_password = bcrypt.hashpw(password,bcrypt.gensalt(14))
    return hashed_password.encode('utf-8')
x = generate_salt_and_hash("hello")
print(type(x))
print(x)
