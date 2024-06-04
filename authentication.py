import json
import re

class Auth:
    def __init__(self):
        self.database = {
            "users": []
        }  # Simulated database

    def is_username_unique(self, username):
        for user in self.database["users"]:
            if user["username"] == username:
                return False
        return True

    def is_email_unique(self, email):
        for user in self.database["users"]:
            if user["email"] == email:
                return False
        return True

    def validate_username(self, username):
        if not re.match(r'^[A-Za-z0-9]+$', username): #alphanumeric
            return False, "Username must consist of upper and lower case letters and numbers."
        if len(username) > 100:
            return False, "Username length should not be more than 100 characters."
        if not self.is_username_unique(username):
            return False, "Username must be unique."
        return True, ""

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return False, "Email format is invalid."
        if not self.is_email_unique(email):
            return False, "Email must be unique."
        return True, ""

    def validate_password(self, password):
        if len(password) <= 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r'[A-Za-z]', password):
            return False, "Password must contain at least two letters."
        if not re.search(r'[@#&$]', password):
            return False, "Password must contain at least one special character (@#&$)."
        return True,""
    
