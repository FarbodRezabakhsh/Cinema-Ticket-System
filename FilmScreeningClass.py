from sql_connecter import *
from ErrorHandeling import Define_FilmScreening_Error
from Define_FilmScreening_Handeling import*
class FilmScreening:
    def __init__(self, FilmScreeningID, MovieID, SalonID, ShowDate):
        self.FilmScreeningID = FilmScreeningID
        self.MovieID = MovieID
        self.SalonID = SalonID
        self.ShowDate = ShowDate

    def Define_FilmScreening(self):
        '''
        Insert Into FilmScreenings Table New_FilmScreening
        '''
        if not Define_FilmScreening_Handeling(self.MovieID, self.SalonID, self.ShowDate):
            raise Define_FilmScreening_Error
        querry = '''INSERT INTO FilmScreenings(MovieID, SalonID, ShowDate)
                    VALUES (%s, %s, %s)'''
        val = (self.MovieID, self.SalonID, self.ShowDate)
        Exe(querry , val)

    def Delete_FilmScreening(self):
        '''
        Delete from FilmScreenings Table Old_FilmScreening
        '''
        querry = '''DELETE FROM FilmScreenings
                    WHERE FilmScreeningID = %s'''
        val = (self.FilmScreeningID, )
        Exe(querry, val)
