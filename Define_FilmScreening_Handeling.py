from datetime import datetime
from sql_connecter import *


def Define_FilmScreening_Handeling(MovieID, SalonID, ShowDate):
    querry = '''
    select  movies.ShowTime
    from movies
    where MovieID = %s
    '''
    val = (MovieID, )
    mycursor = mydb.cursor()
    mycursor.execute(querry, val)
    MovieShowTime = mycursor.fetchall()[0][0]

    querry = '''
    select filmscreenings.ShowDate , movies.ShowTime
    from filmscreenings
    join movies
    on filmscreenings.MovieID = movies.MovieID
    where filmscreenings.SalonId = %s
    order by filmscreenings.ShowDate 
    '''
    val = (SalonID,)
    mycursor = mydb.cursor()
    mycursor.execute(querry, val)
    myresult = mycursor.fetchall()

    check = False
    if myresult == []:
        check = True
    ShowDate = datetime.strptime(ShowDate, '%Y-%m-%d %H:%M:%S')
    for i in range(len(myresult) - 1):
        if myresult[i][0] + myresult[i][1] < ShowDate and myresult[i+1][0] + myresult[i+1][1] > ShowDate + MovieShowTime:
            check = True
            break
    if not check:
        if myresult[-1][0] + myresult[-1][1] < ShowDate:
            check = True
        elif ShowDate + MovieShowTime < myresult[0][0]:
            check = True

    return check