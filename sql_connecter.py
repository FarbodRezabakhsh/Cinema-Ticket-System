import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="13791227",
  database="CinemaDB"
)

def Exe(querry , val):
  mycursor = mydb.cursor()
  mycursor.execute(querry, val)
  mydb.commit()

def Get(querry):
  mycursor = mydb.cursor()
  mycursor.execute(querry)
  myresult = mycursor.fetchall()
  return(myresult)