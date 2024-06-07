from sql_connecter import *
class Movie:
    def __init__(self, MovieID, MovieName, AgeRating, ShowTime):
        '''
        Constructs:
        MovieID : int 
        MovieName : str
        AgeRating : int
        ShowTime : str
        '''
        self.MovieID = MovieID
        self.MovieName = MovieName
        self.AgeRating = AgeRating
        self.ShowTime = ShowTime

    def Define_Movie(self):
        '''
        Insert Into Movies Table New_Movie
        '''
        querry = '''INSERT INTO Movies(MovieName, AgeRating, ShowTime)
                    VALUES (%s, %s, %s)''' 
        val = (self.MovieName, self.AgeRating, self.ShowTime)
        Exe(querry, val)

    def Delete_Movie(self):
        querry = '''DELETE FROM Movies
                    WHERE MovieID = %s'''
        val = (self.MovieID, )
        Exe(querry , val)