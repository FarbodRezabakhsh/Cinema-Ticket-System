import re
import sqlite3
from typing import Dict, Tuple

class Auth:
    """
    A class for handling user authentication, including signing up, logging in, 
    and resetting passwords. This class interacts with an SQLite database to 
    store and retrieve user information.
    """
    def __init__(self, database_path: str) -> None:
        """
        Attributes:
        db_path (str): The path to the SQLite database file.
        conn (sqlite3.Connection): The SQLite database connection.
        c (sqlite3.Cursor): The cursor for executing SQL commands.
        """
        self.db_path = database_path
        self.conn = sqlite3.connect(database_path)
        self.c = self.conn.cursor()

    def add_to_database(self, user_data: Dict[str, str]) -> Dict[str, str]:
        """
        Add a user to the database.

        Args:
            user_data (Dict[str, str]): A dictionary containing 'username', 'email', and 'password' of the user.

        Returns:
            Dict[str, str]: A dictionary containing the status and message of the operation.
        """
        try:
            self.c.execute("INSERT INTO USERS(username,email,password) VALUES (?,?,?)",
                           (user_data['username'], user_data['email'], user_data['password']))
            self.conn.commit()
            return {'status': 'success', 'message': 'user added to database.'}
        except sqlite3.Error as e:
            return {'status': 'fail', 'message': f'error adding to database {e}'}

    def is_username_unique(self, username: str) -> bool:
        """
        Check if the username is unique.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username is unique, False otherwise.
        """
        for user in self.database["users"]:
            if user["username"] == username:
                return False
        return True

    def is_email_unique(self, email: str) -> bool:
        """
        Check if the email is unique.

        Args:
            email (str): The email to check.

        Returns:
            bool: True if the email is unique, False otherwise.
        """
        for user in self.database["users"]:
            if user["email"] == email:
                return False
        return True

    def validate_username(self, username: str) -> bool:
        """
        Validate the username format and uniqueness.

        Args:
            username (str): The username to validate.

        Returns:
            bool: A tuple containing a boolean indicating validity and a message.
        """
        if not re.match(r'^[A-Za-z0-9]+$', username):  # alphanumeric
            return False, "Username must consist of upper and lower case letters and numbers."
        if len(username) > 100:
            return False, "Username length should not be more than 100 characters."
        if not self.is_username_unique(username):
            return False, "Username must be unique."
        return True

    def validate_email(self, email: str) -> bool:
        """
        Validate the email format and uniqueness.

        Args:
            email (str): The email to validate.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating validity and a message.
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return False, "Email format is invalid."
        if not self.is_email_unique(email):
            return False, "Email must be unique."
        return True

    def validate_password(self, password: str) -> bool:
        """
        Validate the password format.

        Args:
            password (str): The password to validate.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating validity and a message.
        """
        if len(password) <= 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r'[A-Za-z]', password):
            return False, "Password must contain at least two letters."
        if not re.search(r'[@#&$]', password):
            return False, "Password must contain at least one special character (@#&$)."
        return True

    def sign_up(self, username: str, email: str, password: str) -> Dict[str, str]:
        """
        Sign up a new user by validating inputs and adding to the database.

        Args:
            username (str): The username of the new user.
            email (str): The email of the new user.
            password (str): The password of the new user.

        Returns:
            Dict[str, str]: A dictionary containing the status and message of the operation.
        """
        try:
            self.validate_username(username)
        except ValueError as ve:
            raise ValueError(f'Username is wrong! {ve}')
        try:
            self.validate_email(email)
        except ValueError as ve:
            raise ValueError(f'Email is wrong. {ve}')
        try:
            self.validate_password(password)
        except ValueError as ve:
            raise ValueError(f'Password you entered is wrong! {ve}')

        user_data = {
            "username": username,
            "email": email,
            "password": password,
        }

        return self.add_to_database(user_data)

    def login(self, username: str, password: str) -> Dict[str, str]:
        """
        Log in a user by validating the username and password.
        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            Dict[str, str]: A dictionary containing the status and message of the operation.
        """
        try:
            self.c.execute("SELECT * FROM USERS WHERE username = ? AND password = ?", (username, password))
            user = self.c.fetchone()
            if user:
                return {'status': 'success', 'message': 'Login successful.'}
            else:
                return {'status': 'fail', 'message': 'Invalid username or password.'}
        except sqlite3.Error as e:
            return {'status': 'fail', 'message': f'Error logging in: {e}'}

    def reset_password(self, username: str, old_password: str, new_password: str, confirm_password: str) -> Dict[str, str]:
        """
        Reset the password for a user.
        Args:
            username (str): The username of the user.
            old_password (str): The old password of the user.
            new_password (str): The new password of the user.
            confirm_password (str): The confirmation of the new password.

        Returns:
            Dict[str, str]: A dictionary containing the status and message of the operation.
        """
        self.c.execute("SELECT password FROM USERS WHERE username=?", (username,))
        row = self.c.fetchone()
        if row is None:
            return {'status': 'fail', 'message': 'User not found.'}

        if row[0] != old_password:
            return {'status': 'fail', 'message': 'Old password is incorrect.'}

        if new_password != confirm_password:
            return {'status': 'fail', 'message': 'New password and confirm password do not match.'}
        try:
            self.c.execute("UPDATE USERS SET password = ? WHERE username = ?", (new_password, username))
            self.conn.commit()
            return {'status': 'success', 'message': 'Password reset successful.'}
        except sqlite3.Error as e:
            return {'status': 'fail', 'message': f'Error resetting password: {e}'}
