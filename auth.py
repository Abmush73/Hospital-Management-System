import hashlib
import secrets

import database
from user import User


def hash_password(password):
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200000).hex()
    return f"{salt}${hashed}"


def verify_password(password, stored_hash):
    salt, hashed = stored_hash.split("$")
    check = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200000).hex()
    return secrets.compare_digest(check, hashed)


def login(username, password):
    record = database.get_user_credentials(username)
    if record is None:
        return None
    user_id, username, stored_hash, role, doctor_id = record
    if not verify_password(password, stored_hash):
        return None
    return User(user_id, username, role, doctor_id)
