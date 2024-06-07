create database CINEMADB;
use CINEMADB;

-- Table for Wallets
CREATE TABLE Wallets (
    WalletID INT PRIMARY KEY auto_increment,
    CardNumber VARCHAR(20),
    WalletPassword VARCHAR(255),
    CVV2 VARCHAR(4),
    Balance FLOAT
);

-- Table for Subscriptions
CREATE TABLE Subscriptions (
    SubscriptionID INT PRIMARY KEY auto_increment,
    SubscriptionType VARCHAR(50),
    ExpiryDate DATE,
    SubscriptionInfo TEXT,
    Price float
);

-- Table for Users
CREATE TABLE Users (
    UserID int primary key auto_increment,
    Username VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    Name VARCHAR(255),
    PhoneNumber VARCHAR(20),
    Email VARCHAR(255) UNIQUE ,
    Birthday DATE,
    RegistrationMonthYear VARCHAR(7),
    RegistrationDate DATE,
    WalletID INT,
    SubscriptionID INT,
    IsAdmin BOOLEAN,
    FOREIGN KEY (WalletID) REFERENCES Wallets(WalletID) on delete restrict ,
    FOREIGN KEY (SubscriptionID) REFERENCES Subscriptions(SubscriptionID) on delete cascade
);


-- Table for Salons
CREATE TABLE Salons (
    SalonID INT PRIMARY KEY auto_increment,
    RowCount INT,
    ColumnCount INT,
    TicketPrice FLOAT
);

-- Table for Movies
CREATE TABLE Movies (
    MovieID INT PRIMARY KEY auto_increment,
    MovieName VARCHAR(255),
    AgeRating INT,
    ShowTime TIME
);


-- Table for Tickets
CREATE TABLE Tickets (
    TicketID INT PRIMARY KEY auto_increment,
    FilmScreeningID INT,
    UserID int,
    SeatRow INT,
    SeatColumn INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (FilmScreeningID) REFERENCES FilmScreenings(FilmScreeningID) ON DELETE CASCADE
);



-- Table for FilmScreening
CREATE TABLE FilmScreenings (
    FilmScreeningID INT PRIMARY KEY auto_increment,
    MovieID INT,
    SalonID INT,
    ShowDate DATETIME,
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID) on delete CASCADE,
    FOREIGN KEY (SalonID) REFERENCES Salons(SalonID) on delete CASCADE
);

-- Table for Comments
CREATE TABLE Comments (
    CommentID INT PRIMARY KEY auto_increment,
    MovieID INT,
    UserID int,
    CommentText TEXT,
    ReplyTo INT,
    CommentDate DATE,
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ReplyTo) REFERENCES Comments(CommentID) on delete cascade
);

-- Table for Ratings
CREATE TABLE Ratings (
    RatingID INT PRIMARY KEY auto_increment,
    UserID int,
    MovieID INT,
    StarRating VARCHAR(5),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
);