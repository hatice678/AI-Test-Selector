def create_user(username):
    if not username:
        raise ValueError("Username cannot be empty")
    return {"username": username, "active": True}
