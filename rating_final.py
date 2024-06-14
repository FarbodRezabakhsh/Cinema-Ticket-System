import mysql
import mysql.connector

class Rating:
    def __init__(self,user_id, star_rating, movie_id):
      
        self.user_id = user_id
        self.star_rating = star_rating
        self.movie_id = movie_id
    def define_Rating(self,user_id,star_rating,movie_id):
      Insert INTO ratings(UserID, MovieID, StarRating) values (%s, %s, %s)


      val = (self.UserID, self.MovieID, StarRating)

  
      exec(query,val)


      cursor.close()
      conn.close()
