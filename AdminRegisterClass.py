from mysql_conncetor import Exe,Get
import mysql.connector
from typing import Dict, Tuple
import re

class Admin:
    def __init__(self) -> None:
        self.db_name = 'CinemaDB'
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fare***12",
            database=self.db_name
        )
        self.c = self.conn.cursor()

    def validate_email(self, email: str) -> Tuple[bool, str]:
        """
        Validate the email format and uniqueness.
        Args:
            email (str).
        Returns:
            Tuple[bool, str].
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return False, "Email format is invalid."
        return True, ""

    def validate_password(self, password: str) -> Tuple[bool, str]:
        """
        Validate the password format.
        Args:
            password (str)
        Returns:
            Tuple[bool, str]
        """
        if len(password) <= 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r'[A-Za-z]', password):
            return False, "Password must contain at least two letters."
        if not re.search(r'[@#&$]', password):
            return False, "Password must contain at least one special character (@#&$)."
        return True,""
    
    def register(self, username: str, email: str, password: str, admin: bool = True) -> dict:
        try:
            valid, msg = self.validate_email(email)
            if not valid:
                return {'status': 'fail', 'message': f'Email validation failed: {msg}'}
            valid, msg = self.validate_password(password)
            if not valid:
                return {'status': 'fail', 'message': f'Password validation failed: {msg}'}
            #check if user already exists
            self.c.execute("SELECT * FROM USERS WHERE username = %s OR email = %s", (username, email))
            user = self.c.fetchone()
            if user:
                return {'status': 'fail', 'message': 'Username or email already exists.'}
            Exe("INSERT INTO USERS (username, email, password, IsAdmin) VALUES (%s, %s, %s, %s)",
                (username, email, password, admin))
            self.conn.commit()
            return {'status': 'success', 'message': 'User registered successfully!.'}
        except mysql.connector.Error as e:
            return {'status': 'fail', 'message': f'Error registering user: {e}'}


if __name__ == '__main__':
    admin = Admin()
    username = "gorge"
    email = "gorge@gmail.com"
    password = "gorge@1234"
    result = admin.register(username, email, password)
    print(result)
