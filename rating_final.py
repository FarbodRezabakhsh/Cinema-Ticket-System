import mysql
class Rating:
    def __init__(self,user_id, star_rating, movie_id):
      
        self.user_id = user_id
        self.star_rating = star_rating
        self.movie_id = movie_id
    def define_Rating(self,user_id,star_rating,movie_id):
      query='''insert into rating(user_id,star_rating,movie_id)
      VALUES (%s, %s, %s)'''

       
  
      exec(query,val)

      cursor.close()
      conn.close()
