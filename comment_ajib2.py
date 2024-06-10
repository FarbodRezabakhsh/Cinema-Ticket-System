import import mysql
from datetime import datetime

class Comment:
    comment: str
    user_id: int
    clease_date: datetime
    replomment_id: int
    rey: str = None

    def __init__(self, comment: str, user_id: int, comment_id: int, release_date: datetime, reply: str = None):
        self.comment = comment
        self.user_id = user_id
        self.comment_id = comment_id
        self.release_date = release_date
        self.reply = reply
    def define_comment(comment,user_id,comment_id,relase,date,reply):   
        
        
     query = '''
        INSERT INTO Comments (CommentID, UserID, CommentText, CommentDate, ReplyText,None)
        VALUES (%s, %s, %s, %s, %s)
        '''
        exec(query,val)

        cursor.close()
        conn.close()

    def delete(self,comment_id):
        false_comment= comment (comment_id)
        false_comment.delete()
                query = '''
        DELETE FROM Comments
        WHERE CommentID = %s
        '''
        cursor.execute(query, (comment_id,))
        conn.commit()
    val=(self,comment_id)
    
    cursor.close()
        conn.close()

