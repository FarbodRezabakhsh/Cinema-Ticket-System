import  sqlite3

def create_tables():
    conn = sqlite3.connect('cinema_ticket.db')
    cursor = conn.cursor()

    cursor.execute('''
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

    cursor.execute('''
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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Subscriptions (
        SubscriptionID INTEGER PRIMARY KEY AUTOINCREMENT,
        SubscriptionType TEXT,
        ExpiryDate DATE,
        SubscriptionInfo TEXT,
        UserID TEXT,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cinemas (
        CinemaID INTEGER PRIMARY KEY AUTOINCREMENT,
        CinemaName TEXT,
        Location TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Salons (
        SalonID INTEGER PRIMARY KEY AUTOINCREMENT,
        RowCount INTEGER,
        ColumnCount INTEGER,
        TicketPrice FLOAT,
        CinemaID INTEGER,
        FOREIGN KEY (CinemaID) REFERENCES Cinemas(CinemaID)
    )
    ''')

    cursor.execute('''
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

    cursor.execute('''
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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Comments (
        CommentID INTEGER PRIMARY KEY AUTOINCREMENT,
        MovieID INTEGER,
        CommentText TEXT,
        ReplyText TEXT,
        CommentDate DATE,
        FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ratings (
        RatingID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID TEXT,
        StarRating TEXT,
        MovieID INTEGER,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print("Tables created successfully")
