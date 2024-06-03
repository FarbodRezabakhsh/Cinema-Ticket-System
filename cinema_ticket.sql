-- Create the database
CREATE DATABASE cinema_ticket;

-- Switch to the database
USE cinema_ticket;

-- Create the User table
CREATE TABLE Users (
    UserID VARCHAR(50) PRIMARY KEY,
    Password VARCHAR(255),
    Name VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(255),
    Birthday DATE,
    RegistrationMonthYear VARCHAR(7),
    RegistrationDate DATE,
    WalletID INT,
    SubscriptionID INT,
    IsAdmin BOOLEAN,
    FOREIGN KEY (WalletID) REFERENCES Wallets(WalletID),
    FOREIGN KEY (SubscriptionID) REFERENCES Subscriptions(SubscriptionID)
);

-- Create the Wallet table
CREATE TABLE Wallets (
    WalletID INT AUTO_INCREMENT PRIMARY KEY,
    CardNumber VARCHAR(20),
    WalletPassword VARCHAR(255),
    CVV2 VARCHAR(4),
    Balance FLOAT,
    UserID VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Create the Subscription table
CREATE TABLE Subscriptions (
    SubscriptionID INT AUTO_INCREMENT PRIMARY KEY,
    SubscriptionType VARCHAR(50),
    ExpiryDate DATE,
    SubscriptionInfo TEXT,
    UserID VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Create the Cinema table
CREATE TABLE Cinemas (
    CinemaID INT AUTO_INCREMENT PRIMARY KEY,
    MovieID INT,
    SalonID INT,
    ShowDate DATE,
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
    FOREIGN KEY (SalonID) REFERENCES Salons(SalonID)
);

-- Create the Salon table
CREATE TABLE Salons (
    SalonID INT AUTO_INCREMENT PRIMARY KEY,
    RowCount INT,
    ColumnCount INT,
    TicketPrice FLOAT
);

-- Create the Movie table
CREATE TABLE Movies (
    MovieID INT AUTO_INCREMENT PRIMARY KEY,
    MovieName VARCHAR(255),
    AgeRating INT,
    CinemaID INT,
    ShowTime TIME,
    FOREIGN KEY (CinemaID) REFERENCES Cinemas(CinemaID)
);

-- Create the Ticket table
CREATE TABLE Tickets (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    SalonID INT,
    UserID VARCHAR(50),
    MovieID INT,
    SeatRow INT,
    SeatColumn INT,
    FOREIGN KEY (SalonID) REFERENCES Salons(SalonID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
);

-- Create the Comment table
CREATE TABLE Comments (
    CommentID INT AUTO_INCREMENT PRIMARY KEY,
    MovieID INT,
    CommentText TEXT,
    ReplyText TEXT,
    CommentDate DATE,
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
);

-- Create the Rate table
CREATE TABLE Ratings (
    RatingID INT AUTO_INCREMENT PRIMARY KEY,
    UserID VARCHAR(50),
    StarRating VARCHAR(5),
    MovieID INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
);
