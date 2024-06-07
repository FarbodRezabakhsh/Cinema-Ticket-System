from sql_connecter import *
from SalonClass import Salon
from FilmScreeningClass import FilmScreening
from MovieClass import Movie

class Admin:
    '''    
    A class to represent a person.

    Attributes
    ----------
    UserID : int
    '''
    def __init__(self , UserID):
        '''
        Constructs:
        UserID : int
        '''
        self.UserID = UserID
    
    def Define_Salon(self, RowCount, ColumnCount, TicketPrice):
        '''
        Creat New_Salon Obj And Call Define_Salon Method from Salon Class.
        '''
        New_Salon = Salon('DEFAULT', RowCount, ColumnCount, TicketPrice)
        New_Salon.Define_Salon()

    def Define_Movie(self, MovieName, AgeRating, ShowTime):
        '''
        Creat New_Movie Obj And Call Define_Movie Method from Movie Class.
        '''
        New_Movie = Movie('DEFAULT', MovieName, AgeRating, ShowTime)
        New_Movie.Define_Movie()

    def Define_FilmScreening(self, MovieID, SalonID, ShowDate):
        New_FilmScreening = FilmScreening('DEFAULT', MovieID, SalonID, ShowDate)
        New_FilmScreening.Define_FilmScreening()
    
    def Delete_Salon(self, SalonID):
        Old_Salon = Salon(SalonID, None, None, None)
        Old_Salon.Delete_Salon()

    def Delete_Movie(self, MovieID):
        Old_Movie = Movie(MovieID, None, None, None)
        Old_Movie.Delete_Movie()

    def Delete_FilmScreening(self, FilmScreeningID):
        Old_FilmScreening = FilmScreening(FilmScreeningID, None, None, None)
        Old_FilmScreening.Delete_FilmScreening()
    
    def Get_All_Movies(self):
        querry = ('''SELECT * 
                FROM Movies''')
        return Get(querry)

    def Get_All_Salons(self):
        querry = ('''SELECT * 
                    FROM Salons''')
        return Get(querry)
   
    def Get_All_FilmScreenings(self):
        querry = ('''SELECT * 
                FROM FilmScreenings''')
        return Get(querry)



