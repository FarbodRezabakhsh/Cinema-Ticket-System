from sql_connecter import *

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
        querry = '''DELETE FROM Movies
                    WHERE MovieID = %s'''
        val = (self.MovieID, )
        Exe(querry , val)

    def Get_All_Movies():
        '''
        Return All FilmScreenings from FilmScreenings table.
        '''    
        querry = ('''SELECT FilmScreeningID , m.MovieID , m.MovieName , s.SalonID , s.TicketPrice
                    FROM FilmScreenings
                    join cinemadb.movies m on m.MovieID = FilmScreenings.MovieID
                    join cinemadb.salons s on s.SalonID = FilmScreenings.SalonID''')
        return Get(querry)