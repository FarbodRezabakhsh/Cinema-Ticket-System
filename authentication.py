import re
import sqlite3

class Auth:
    def __init__(self, database_path):
        self.db_path = database_path
        self.conn = sqlite3.connect(database_path)
        self.c = self.conn.cursor()

    def add_to_database(self, user_data):
        try:
            self.c.execute("INSERT INTO USERS(username,email,password) VALUES (?,?,?)",
                           (user_data['username'], user_data['email'], user_data['password']))
            self.conn.commit()
            return {'status': 'success', 'message': 'user added to database.'}
        except sqlite3.Error as e:
            return {'status': 'fail', 'message': f'error adding to database {e}'}

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
        if not re.match(r'^[A-Za-z0-9]+$', username):  # alphanumeric
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
        return True, ""

    def sign_up(self, username, email, password):
        is_valid, msg = self.validate_username(username)
        if not is_valid:
            return {"status": "fail", "message": msg}

        is_valid, msg = self.validate_email(email)
        if not is_valid:
            return {"status": "fail", "message": msg}

        is_valid, msg = self.validate_password(password)
        if not is_valid:
            return {"status": "fail", "message": msg}

        user_data = {
            "username": username,
            "email": email,
            "password": password,
        }

        return self.add_to_database(user_data)

    def login(self, username, password):
        try:
            self.c.execute("SELECT * FROM USERS WHERE username = ? AND password = ?", (username, password))
            user = self.c.fetchone()
            if user:
                return {'status': 'success', 'message': 'Login successful.'}
            else:
                return {'status': 'fail', 'message': 'Invalid username or password.'}
        except sqlite3.Error as e:
            return {'status': 'fail', 'message': f'Error logging in: {e}'}
