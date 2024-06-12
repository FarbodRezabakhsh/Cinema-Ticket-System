from sql_connecter import *
from DeletingHandeling import *

class Movie:
    '''    
    A class to represent Movie.
    '''
    def __init__(self, MovieID : int, MovieName : str, AgeRating : int, ShowTime : str):
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
        '''
        Delete from Movies Table Old_Movie
        '''
        res = Delete_Movie_Handler(self.MovieID)
        querry = '''DELETE FROM Movies
                    WHERE MovieID = %s'''
        val = (self.MovieID, )
        Exe(querry , val)
        return res

    def Get_All_Movies():
        '''
        Return All Movies from Movies table.
        '''    
        querry = ('''SELECT *
                    FROM Movies''')
        return Get(querry)