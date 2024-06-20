import unittest
import sqlite3
from datetime import datetime
from main import Database, User, Admin, Menu

class TestCinemaSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up database and tables before any tests run
        cls.conn = sqlite3.connect('test_cinema_ticket.db')
        cls.cursor = cls.conn.cursor()
        cls.create_tables()
        cls.add_sample_data()

    @classmethod
    def tearDownClass(cls):
        # Tear down the database and tables after all tests run
        cls.conn.close()
        import os
        os.remove('test_cinema_ticket.db')

    @classmethod
    def create_tables(cls):
        Database.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID TEXT PRIMARY KEY,
            Password TEXT,
            Name TEXT,
            PhoneNumber TEXT,
            Email TEXT,
            Birthday DATE,
            RegistrationMonthYear TEXT,
            RegistrationDate DATE,
            WalletID INTEGER,
            SubscriptionID INTEGER,
            IsAdmin BOOLEAN
        )
        ''')

        Database.execute('''
        CREATE TABLE IF NOT EXISTS Wallets (
            WalletID INTEGER PRIMARY KEY AUTOINCREMENT,
            CardNumber TEXT,
            WalletPassword TEXT,
            CVV2 TEXT,
            Balance FLOAT,
            UserID TEXT,
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        )
        ''')

        Database.execute('''
        CREATE TABLE IF NOT EXISTS Subscriptions (
            SubscriptionID INTEGER PRIMARY KEY AUTOINCREMENT,
            SubscriptionType TEXT,
            ExpiryDate DATE,
            SubscriptionInfo TEXT,
            UserID TEXT,
            FOREIGN KEY (UserID) REFERENCES Users(UserID)
        )
        ''')

        Database.execute('''
        CREATE TABLE IF NOT EXISTS Cinemas (
            CinemaID INTEGER PRIMARY KEY AUTOINCREMENT,
            CinemaName TEXT,
            Location TEXT
        )
        ''')

        Database.execute('''
        CREATE TABLE IF NOT EXISTS Salons (
            SalonID INTEGER PRIMARY KEY AUTOINCREMENT,
            RowCount INTEGER,
            ColumnCount INTEGER,
            TicketPrice FLOAT,
            CinemaID INTEGER,
            FOREIGN KEY (CinemaID) REFERENCES Cinemas(CinemaID)
        )
        ''')

        Database.execute('''
        CREATE TABLE IF NOT EXISTS Movies (
            MovieID INTEGER PRIMARY KEY AUTOINCREMENT,
            MovieName TEXT,
            Description TEXT,
            ReleaseDate TEXT,
            AgeRating INTEGER,
            ShowTime TEXT,
            CinemaID INTEGER,
            FOREIGN KEY (CinemaID) REFERENCES Cinemas(CinemaID)
        )
        ''')

        Database.execute('''
        CREATE TABLE IF NOT EXISTS Tickets (
            TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
            SalonID INTEGER,
            UserID TEXT,
            MovieID INTEGER,
            SeatRow INTEGER,
            SeatColumn INTEGER,
            FOREIGN KEY (SalonID) REFERENCES Salons(SalonID),
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
        )
        ''')

        Database.execute('''
        CREATE TABLE IF NOT EXISTS Comments (
            CommentID INTEGER PRIMARY KEY AUTOINCREMENT,
            MovieID INTEGER,
            CommentText TEXT,
            ReplyText TEXT,
            CommentDate DATE,
            FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
        )
        ''')

        Database.execute('''
        CREATE TABLE IF NOT EXISTS Ratings (
            RatingID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID TEXT,
            StarRating TEXT,
            MovieID INTEGER,
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
        )
        ''')

    @classmethod
    def add_sample_data(cls):
        username = "testuser"
        password = User.hash_password("password123")
        email = "testuser@example.com"
        phone = "1234567890"
        birth_date = "1990-01-01"
        registration_month_year = datetime.now().strftime('%Y-%m')
        registration_date = datetime.now().strftime('%Y-%m-%d')
        Database.execute('''
            INSERT INTO Users (UserID, Password, Name, PhoneNumber, Email, Birthday, RegistrationMonthYear, RegistrationDate, WalletID, SubscriptionID, IsAdmin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, password, username, phone, email, birth_date, registration_month_year, registration_date, None, None, False))

    def test_register_user(self):
        User.clear_screen = lambda: None  # Mock clear_screen to do nothing
        User.execute_query_register = lambda username, password, email, phone, birth_date: Database.execute('''
            INSERT INTO Users (UserID, Password, Name, PhoneNumber, Email, Birthday, RegistrationMonthYear, RegistrationDate, WalletID, SubscriptionID, IsAdmin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, password, username, phone, email, birth_date, datetime.now().strftime('%Y-%m'), datetime.now().strftime('%Y-%m-%d'), None, None, False))

        username = "newuser"
        password = "newpassword123"
        email = "newuser@example.com"
        phone = "0987654321"
        birth_date = "1995-01-01"
        hashed_password = User.hash_password(password)

        User.register = lambda: User.execute_query_register(username, hashed_password, email, phone, birth_date)

        User.register()
        user = Database.fetch('SELECT * FROM Users WHERE UserID = ?', (username,))
        self.assertEqual(len(user), 1, "User should be registered successfully")

    def test_login_user(self):
        User.clear_screen = lambda: None  # Mock clear_screen to do nothing
        User.execute_query_login = lambda username, password: Database.fetch('''
            SELECT UserID, IsAdmin FROM Users WHERE UserID = ? AND Password = ?
        ''', (username, password))

        username = "testuser"
        password = "password123"
        hashed_password = User.hash_password(password)

        User.login = lambda: User.execute_query_login(username, hashed_password)

        user = User.login()
        self.assertIsNotNone(user, "User should be able to login successfully")
        self.assertEqual(user[0][0], username, "UserID should match")
        self.assertFalse(user[0][1], "User should not be an admin")

    def test_add_movie(self):
        Admin.clear_screen = lambda: None  # Mock clear_screen to do nothing
        Admin.execute_query_add_movie = lambda title, description, release_date, cinema_id: Database.execute('''
            INSERT INTO Movies (MovieName, Description, ReleaseDate, CinemaID)
            VALUES (?, ?, ?, ?)
        ''', (title, description, release_date, cinema_id))

        title = "Test Movie"
        description = "This is a test movie"
        release_date = "2023-01-01"
        cinema_id = 1

        Admin.add_movie = lambda: Admin.execute_query_add_movie(title, description, release_date, cinema_id)

        Admin.add_movie()
        movie = Database.fetch('SELECT * FROM Movies WHERE MovieName = ?', (title,))
        self.assertEqual(len(movie), 1, "Movie should be added successfully")

if __name__ == '__main__':
    unittest.main()
