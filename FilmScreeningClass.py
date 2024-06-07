from sql_connecter import *

class FilmScreening:
    def __init__(self, FilmScreeningID, MovieID, SalonID, ShowDate):
        self.FilmScreeningID = FilmScreeningID
        self.MovieID = MovieID
        self.SalonID = SalonID
        self.ShowDate = ShowDate

    def Define_FilmScreening(self):
        querry = '''INSERT INTO FilmScreenings(MovieID, SalonID, ShowDate)
                    VALUES (%s, %s, %s)'''
        val = (self.MovieID, self.SalonID, self.ShowDate)
        Exe(querry , val)

    def Delete_FilmScreening(self):
        querry = '''DELETE FROM FilmScreenings
                    WHERE FilmScreeningID = %s'''
        val = (self.FilmScreeningID, )
        Exe(querry, val)
