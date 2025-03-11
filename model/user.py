users = {
    "john": "hello",
    "susan": "bye",
    "admin": "admin",
    "faraja": "faraja"
}

def add_user(username, password):
    if username in users:
        return False
    users[username] = password
    return True

def verify_user(username, password):
    actual_password = users.get(username)
    if actual_password and actual_password == password:
        return True
    return False