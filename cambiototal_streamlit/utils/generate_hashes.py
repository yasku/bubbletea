import bcrypt

# Passwords to hash
passwords = [b"admin123", b"operador123"]

# Generate hashes
hashed_passwords = []
for pw in passwords:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw, salt)
    hashed_passwords.append(hashed.decode('utf-8'))

# Print the hashes
print("Generated Hashes:")
for i, h in enumerate(hashed_passwords):
    print(f"Password {i+1}: {h}")
