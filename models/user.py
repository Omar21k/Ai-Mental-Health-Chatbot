from database import add_user_to_db, get_user

# Pre-existing users
DEFAULT_USERS = {
    "john": "hello",
    "susan": "bye",
    "admin": "admin",
    "faraja": "faraja"
}

def initialize_default_users():
    for username, password in DEFAULT_USERS.items():
        add_user_to_db(username, password)

def verify_user(username, password):
    # First check database
    user = get_user(username)
    if user and user[1] == password:
        return True
    
    # Then check default users as fallback
    return DEFAULT_USERS.get(username) == password

def add_user(username, password):
    # Don't allow overwriting default users
    if username in DEFAULT_USERS:
        return False
    return add_user_to_db(username, password)