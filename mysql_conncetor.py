import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Fare***12",
  database="CinemaDB"
)

def Exe(querry : str , val : any):
  mycursor = mydb.cursor()
  mycursor.execute(querry, val)
  mydb.commit()

def Get(querry : str):
  mycursor = mydb.cursor()
  mycursor.execute(querry)
  myresult = mycursor.fetchall()
  return(myresult)

def Get_list(querry : str , val : any):
  mycursor = mydb.cursor()
  mycursor.execute(querry , val)
  myresult = mycursor.fetchall()
  return(myresult)
