from sql_connecter import *

class Rating:
    def __init__(self,UserID, MovieID, StarRating):
        self.UserID = UserID
        self.StarRating = StarRating
        self.MovieID = MovieID

    def define_Rating(self):
        querry = '''
        Insert INTO ratings(UserID, MovieID, StarRating)
        values (%s, %s, %s)'''

        val = (self.UserID, self.MovieID, self.StarRating)

        Exe(querry, val)
