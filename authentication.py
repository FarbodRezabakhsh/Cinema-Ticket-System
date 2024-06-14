import re 
import mysql.connector 
from typing import Dict, Tuple, Any 
from mysql.connector import Error 
 
class Auth: 
    """ 
    A class for handling user authentication, including signing up, logging in,  
    and resetting passwords. This class interacts with a MySQL database to  
    store and retrieve user information. 
    """ 
 
    def init(self) -> None: 
        """ 
        Initialize the Auth class. 
        """ 
        self.db_name = 'CinemaDB' 
        self.conn = self.create_connection() 
 
    def create_connection(self): 
        """ 
        Create a connection to the MySQL database. 
 
        Returns: 
            mysql.connector.connection: A connection object to the MySQL database. 
        """ 
        try: 
            conn = mysql.connector.connect( 
                host="localhost", 
                user="root", 
                password="Fare***12", 
                database=self.db_name 
            ) 
            return conn 
        except Error as e: 
            print(f"Error: {e}") 
            return None 
 
    def execute_query(self, query: str, values: Tuple = None): 
        """ 
        Execute a SQL query on the database. 
 
        Args: 
            query (str): The SQL query to execute. 
            values (Tuple, optional): The values to pass to the SQL query. 
 
        Returns: 
            mysql.connector.cursor: The cursor after executing the query. 
        """ 
        try: 
            cursor = self.conn.cursor() 
            if values: 
                cursor.execute(query, values) 
            else: 
                cursor.execute(query) 
            self.conn.commit() 
            return cursor 
        except Error as e: 
            print(f"Error: {e}") 
            return None 
 
    def fetch_all(self, query: str, values: Tuple = None): 
        """ 
        Execute a SELECT query on the database and return all results. 
 
        Args: 
            query (str): The SELECT SQL query to execute. 
            values (Tuple, optional): The values to pass to the SQL query. 
 
        Returns: 
            list: The results of the query. 
        """ 
        cursor = self.execute_query(query, values) 
        if cursor: 
            return cursor.fetchall() 
        return None 
 
    def add_to_database(self, user_data: Dict[str, str]) -> Dict[str, str]: 
        """ 
        Add a user to the database. 
 
        Args: 
            user_data (Dict[str, str]): A dictionary containing 'username', 'email', and 'password' of the user. 
 
        Returns: 
            Dict[str, str]: A dictionary containing the status and message of the operation. 
        """ 
        query = "INSERT INTO USERS(username, email, password) VALUES (%s, %s, %s)" 
        if self.execute_query(query, (user_data['username'], user_data['email'], user_data['password'])): 
            return {'status': 'success', 'message': 'User added to database.'} 
        else: 
            return {'status': 'fail', 'message': 'Error adding to database.'} 
 
    def is_username_unique(self, username: str) -> bool: 
        """ 
        Check if the username is unique. 
 
        Args: 
            username (str): The username to check. 
 
        Returns: 
            bool: True if the username is unique, False otherwise. 
        """ 
        query = "SELECT * FROM USERS WHERE username = %s" 
        result = self.fetch_all(query, (username,)) 
        return len(result) == 0 
 
    def is_email_unique(self, email: str) -> bool: 
        """ 
        Check if the email is unique. 
 
        Args: 
            email (str): The email to check. 
 
        Returns: 
            bool: True if the email is unique, False otherwise. 
        """ 
        query = "SELECT * FROM USERS WHERE email = %s" 
        result = self.fetch_all(query, (email,))
        return len(result) == 0 
    
    def validate_username(self, username: str) -> Tuple[bool, str]: 
        """ 
        Validate the username format and uniqueness. 
 
        Args: 
            username (str): The username to validate. 
 
        Returns: 
            Tuple[bool, str]: A tuple containing a boolean indicating validity and a message. 
        """ 
        if not re.match(r'^[A-Za-z0-9]+$', username):  # alphanumeric 
            return False, "Username must consist of upper and lower case letters and numbers." 
        if len(username) > 100: 
            return False, "Username length should not be more than 100 characters." 
        if not self.is_username_unique(username): 
            return False, "Username must be unique." 
        return True, "Username is valid." 
 
    def validate_email(self, email: str) -> Tuple[bool, str]: 
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
        return True, "Email is valid." 
 
    def validate_password(self, password: str) -> Tuple[bool, str]: 
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
        return True, "Password is valid." 
 
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
        is_valid, message = self.validate_username(username) 
        if not is_valid: 
            return {'status': 'fail', 'message': f'Username error: {message}'} 
 
        is_valid, message = self.validate_email(email) 
        if not is_valid: 
            return {'status': 'fail', 'message': f'Email error: {message}'} 
 
        is_valid, message = self.validate_password(password) 
        if not is_valid: 
            return {'status': 'fail', 'message': f'Password error: {message}'} 
 
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
        query = "SELECT * FROM USERS WHERE username = %s AND password = %s"
        result = self.fetch_all(query, (username, password)) 
        if result: 
            return {'status': 'success', 'message': 'Login successful.'} 
        else: 
            return {'status': 'fail', 'message': 'Invalid username or password.'} 
        
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
        query = "SELECT password FROM USERS WHERE username = %s" 
        result = self.fetch_all(query, (username,)) 
        if not result: 
            return {'status': 'fail', 'message': 'User not found.'} 
 
        if result[0][0] != old_password: 
            return {'status': 'fail', 'message': 'Old password is incorrect.'} 
 
        if new_password != confirm_password: 
            return {'status': 'fail', 'message': 'New password and confirm password do not match.'} 
 
        if not self.validate_password(new_password)[0]: 
            return {'status': 'fail', 'message': 'New password is invalid.'} 
 
        query = "UPDATE USERS SET password = %s WHERE username = %s" 
        if self.execute_query(query, (new_password, username)): 
            return {'status': 'success', 'message': 'Password reset successful.'} 
        else: 
            return {'status': 'fail', 'message': 'Error resetting password.'} 
 
    # Separate database functions 
 
    def Exe(query: str, values: Any) -> None: 
        """ 
        Execute an SQL query on the database. 
    
        Args: 
            query (str): The SQL query to execute. 
            values (Any): The values to pass to the SQL query. 
        """ 
        mydb = mysql.connector.connect( 
            host="localhost", 
            user="root", 
            password="Fare***12", 
            database="CinemaDB" 
        ) 
        try: 
            cursor = mydb.cursor() 
            cursor.execute(query, values) 
            mydb.commit() 
        except Error as e: 
            print(f"Error: {e}") 
        finally: 
            cursor.close() 
            mydb.close() 
    
    def Get(query: str) -> list: 
        """ 
        Execute a SELECT query on the database and return the results. 
    
        Args: 
            query (str): The SELECT SQL query to execute. 
    
        Returns: 
            list: The results of the query. 
        """ 
        mydb = mysql.connector.connect( 
            host="localhost", 
            user="root", 
            password="Fare***12", 
            database="CinemaDB" 
        ) 
        try: 
            cursor = mydb.cursor() 
            cursor.execute(query) 
            result = cursor.fetchall() 
            return result 
        except Error as e: 
            print(f"Error: {e}") 
            return [] 
        finally: 
            cursor.close() 
            mydb.close() 
    
    def Get_list(query: str, values: Any) -> list: 
        """ 
        Execute a SELECT query on the database with parameters and return the results. 
    
        Args: 
            query (str): The SELECT SQL query to execute. 
            values (Any): The values to pass to the SQL query. 
    
        Returns: 
            list: The results of the query. 
        """ 
        mydb = mysql.connector.connect( 
            host="localhost", 
            user="root", 
            password="Fare***12", 
            database="CinemaDB" 
        ) 
        try: 
            cursor = mydb.cursor() 
            cursor.execute(query, values) 
            result = cursor.fetchall() 
            return result 
        except Error as e: 
            print(f"Error: {e}") 
            return [] 
        finally: 
            cursor.close() 
            mydb.close()
    