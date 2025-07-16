USERS = {
    "admin": {"password": "1234", "role": "admin"},
    "hr": {"password": "hr123", "role": "hr"}
}

def validate_user(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        return user
    return None
