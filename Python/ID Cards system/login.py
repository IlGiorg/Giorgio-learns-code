from creds import valid_users

def loginfn(username, password):
    if username in valid_users and valid_users[username] == password:
        return True
    else:
        return False
