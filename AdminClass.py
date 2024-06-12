from SalonClass import Salon
from FilmScreeningClass import FilmScreening
from MovieClass import Movie
from sql_connecter import *
from ErrorHandeling import *

class Admin:
    '''    
    A class to represent Admin.
    '''
    def __init__(self , UserID : int):
        '''
        Constructs:
        UserID : int
        '''
        self.UserID = UserID
    
    def Define_Salon(self, RowCount : int, ColumnCount : int, TicketPrice : float):
        '''
        Create New_Salon Obj And Call Define_Salon Method from Salon Class.
        '''
        New_Salon = Salon('DEFAULT', RowCount, ColumnCount, TicketPrice)
        New_Salon.Define_Salon()

    def Define_Movie(self, MovieName : str, AgeRating : int, ShowTime : str):
        '''
        Create New_Movie Obj And Call Define_Movie Method from Movie Class.
        '''
        New_Movie = Movie('DEFAULT', MovieName, AgeRating, ShowTime)
        New_Movie.Define_Movie()

    def Define_FilmScreening(self, MovieID : int, SalonID : int, ShowDate : str):
        '''
        Create New_FilmScreening Obj And Call Define_FilmScreening Method from FilmScreening Class.
        If There is interference return you can't do that!
        '''
        try:
            New_FilmScreening = FilmScreening('DEFAULT', MovieID, SalonID, ShowDate)
            New_FilmScreening.Define_FilmScreening()
            return 
        except Define_FilmScreening_Error_interference as er:
            return er
        except Define_FilmScreening_Error_MovieID as er:
            return er
        except Define_FilmScreening_Error_SalonID as er:
            return er
    
    def Delete_Salon(self, SalonID : int):
        '''
        Create Old_Salon Obj And Call Delete_Salon Method from Salon Class.
        '''
        Old_Salon = Salon(SalonID, None, None, None)
        Old_Salon.Delete_Salon()

    def Delete_Movie(self, MovieID : int):
        '''
        Create Old_Movie Obj And Call Delete_Movie Method from Movie Class.
        '''
        Old_Movie = Movie(MovieID, None, None, None)
        Old_Movie.Delete_Movie()

    def Delete_FilmScreening(self, FilmScreeningID : int):
        '''
        Create Old_FilmScreening Obj And Call Delete_FilmScreening Method from FilmScreening Class.
        '''
        Old_FilmScreening = FilmScreening(FilmScreeningID, None, None, None)
        Old_FilmScreening.Delete_FilmScreening()
    
    def Get_All_Movies(self):
        '''
        Return All Movies from Movies table.
        '''        
        querry = ('''SELECT *
                FROM Movies''')
        return Get(querry)

    def Get_All_Salons(self):
        '''
        Return All Salons from Salons table.
        ''' 

        return Salon.Get_All_Salons()
   
    def Get_All_FilmScreenings(self):
        '''
        Return All FilmScreenings from FilmScreenings table.
        '''    
        return Movie.Get_All_Movies()