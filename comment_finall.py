
from datetime import datetime
import mysql.connector

class Comment:
    def init(self, comment: str, user_id: int, comment_id: int, release_date: datetime, reply: str = None):
        self.comment = comment
        self.user_id = user_id
        self.comment_id = comment_id
        self.release_date = release_date
        self.reply = reply

    def define_comment(self, comment, user_id, comment_id, release_date, reply):   
        query = '''
        INSERT INTO Comments (CommentID, UserID, CommentText, CommentDate, ReplyText)
        VALUES (%s, %s, %s, %s, %s)
        '''
        val = (comment_id, user_id, comment, release_date, reply)
        
        conn = mysql.connector.connect(user='yourusername', password='yourpassword', host='localhost', database='yourdatabase')
        cursor = conn.cursor()
        cursor.execute(query, val)
        conn.commit()
        cursor.close()
        conn.close()

    def delete_comment(self, comment_id):
        query = '''
        DELETE FROM Comments
        WHERE CommentID = %s
        '''
        
        conn = mysql.connector.connect(user='yourusername', password='yourpassword', host='localhost', database='yourdatabase')
        cursor = conn.cursor()
        cursor.execute(query, (comment_id,))
        conn.commit()
        cursor.close()
        conn.close()
        