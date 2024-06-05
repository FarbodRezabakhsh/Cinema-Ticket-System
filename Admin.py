import mysql.connector

class Admin:
    def __init__(self , UserID):
        self.UserID = UserID
    
    def Define_Salon(self, RowCount, ColumnCount, TicketPrice):
        New_Salon = Salon('DEFAULT', RowCount, ColumnCount, TicketPrice)
        New_Salon.Define_Salon()

    def Define_Movie(self, MovieName, AgeRating, ShowTime):
        New_Movie = Movie('DEFAULT', MovieName, AgeRating, ShowTime)
        New_Movie.Define_Movie()

    def Define_FilmScreening(self, MovieID, SalonID, ShowDate):
        New_FilmScreening = FilmScreening('DEFAULT', MovieID, SalonID, ShowDate)
        New_FilmScreening.Define_FilmScreening(MovieID, SalonID, ShowDate)
    
    def Delete_Salon(self, SalonID):
        Old_FilmScreening = FilmScreening(SalonID, None, None, None)
        Old_FilmScreening.Delete_FilmScreening()

    def Delete_Movie(self, MovieID):
        Old_Movie = Movie(MovieID, None, None, None)
        Old_Movie.Delete_Movie()

    def Delete_FilmScreening(self, FilmScreeningID):
        Old_FilmScreening = FilmScreening(FilmScreeningID, None, None, None)
        Old_FilmScreening.Delete_FilmScreening()
    
    def Get_All_Movies(self):
        mycursor = mydb.cursor()
        mycursor.execute('''SELECT * 
                            FROM Movies''')
        myresult = mycursor.fetchall()
        return(myresult)

    def Get_All_Salons(self):
        mycursor = mydb.cursor()
        mycursor.execute('''SELECT * 
                            FROM Salons''')
        myresult = mycursor.fetchall()
        return(myresult)
   
    def Get_All_FilmScreenings(self):
        mycursor = mydb.cursor()
        mycursor.execute('''SELECT * 
                            FROM FilmScreenings''')
        myresult = mycursor.fetchall()
        return(myresult)


class Movie:
    def __init__(self, MovieID, MovieName, AgeRating, ShowTime):
        self.MovieID = MovieID
        self.MovieName = MovieName
        self.AgeRating = AgeRating
        self.ShowTime = ShowTime

    def Define_Movie(self):
        mycursor = mydb.cursor()
        querry = '''INSERT INTO Movies(MovieName, AgeRating, ShowTime)
                    VALUES ({}, {}, {})''' .format(self.MovieName, self.AgeRating, self.ShowTime)
        mycursor.execute(querry)
        mydb.commit()


    def Delete_Movie(self):
        mycursor = mydb.cursor()
        querry = '''DELETE FROM Movies
                    WHERE MovieID = {}''' .format(self.MovieID)
        mycursor.execute(querry)
        mydb.commit()

class FilmScreening:
    def __init__(self, FilmScreeningID, MovieID, SalonID, ShowDate):
        self.FilmScreeningID = FilmScreeningID
        self.MovieID = MovieID
        self.SalonID = SalonID
        self.ShowDate = ShowDate

    def Define_FilmScreening(self):
        mycursor = mydb.cursor()
        querry = '''INSERT INTO FilmScreenings(MovieName, AgeRating, ShowTime)
                    VALUES ({}, {}, {})''' .format(self.MovieID, self.SalonID, self.ShowDate)
        mycursor.execute(querry)
        mydb.commit()
        

    def Delete_FilmScreening(self):
        mycursor = mydb.cursor()
        querry = '''DELETE FROM FilmScreenings
                    WHERE FilmScreeningID = {}''' .format(self.FilmScreeningID)
        mycursor.execute(querry)
        mydb.commit()
        
class Salon:
    def __init__(self, SalonID, RowCount, ColumnCount, TicketPrice):
        self.SalonID = SalonID
        self.RowCount = RowCount
        self.ColumnCount = ColumnCount
        self.TicketPrice = TicketPrice
    
    
    def Define_Salon(self):
        mycursor = mydb.cursor()
        querry = '''INSERT INTO Salons(RowCount, ColumnCount, TicketPrice)
                    VALUES ({}, {}, {})''' .format(self.RowCount, self.ColumnCount, self.TicketPrice)
        mycursor.execute(querry)
        mydb.commit()



    def Delet_Salon(self):
        mycursor = mydb.cursor()
        querry = '''DELETE FROM Salons
                    WHERE SalonID = {}''' .format(self.SalonID)
        mycursor.execute(querry)
        mydb.commit()
