from sql_connecter import *
from ErrorHandeling import *
from Define_FilmScreening_Handeling import *

class FilmScreening:
    '''    
    A class to represent FilmScreening.
    '''
    def __init__(self, FilmScreeningID : int, MovieID : int, SalonID : int, ShowDate : str):
        '''
        FilmScreeningID : int
        MovieID : int
        SalonID : int 
        ShowDate : str
        '''
        self.FilmScreeningID = FilmScreeningID
        self.MovieID = MovieID
        self.SalonID = SalonID
        self.ShowDate = ShowDate

    def Define_FilmScreening(self):
        '''
        Insert Into FilmScreenings Table New_FilmScreening If there isn't any interference!
        '''
        not_interference = Define_FilmScreening_Handeling(self.MovieID, self.SalonID, self.ShowDate)
        if not_interference[0]:
            querry = '''INSERT INTO FilmScreenings(MovieID, SalonID, ShowDate)
                        VALUES (%s, %s, %s)'''
            val = (self.MovieID, self.SalonID, self.ShowDate)
            Exe(querry , val)
        else:
            msg = "movieID {} is screening in that time!".format(not_interference[1])
            raise Define_FilmScreening_Error_interference(msg)

    def Delete_FilmScreening(self):
        '''
        Delete from FilmScreenings Table Old_FilmScreening
        '''
        querry = '''DELETE FROM FilmScreenings
                    WHERE FilmScreeningID = %s'''
        val = (self.FilmScreeningID, )
        Exe(querry, val)
