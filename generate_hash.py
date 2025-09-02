import bcrypt

password = b"Veeniths31@"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print(hashed.decode())  # ← This is the hash you will copy
