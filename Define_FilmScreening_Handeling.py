from datetime import datetime
from ErrorHandeling import *
from sql_connecter import *

def Define_FilmScreening_Handeling(MovieID : int, SalonID : int, ShowDate : str):
    '''
    This function check if there is any interference in New_Filmscreening.
    It returns False When there is interference and True When There isn't.
    '''

    querry = '''
    select  movies.ShowTime
    from movies
    where MovieID = %s
    '''
    val = (MovieID, )
    MovieIDs = Get_list(querry , val)
    if MovieIDs == []:
        msg = "There isn't any Movie with MovieID : {}".format(MovieID)
        raise Define_FilmScreening_Error_MovieID(msg)
    MovieShowTime = MovieIDs[0][0]

    querry = '''
    select SalonID
    from Salons
    where SalonID = %s
    '''
    val = (SalonID, )
    SalonIDs = Get_list(querry , val)
    if SalonIDs == []:
        msg = "There isn't any Salon with SalonID : {}".format(SalonID)
        raise Define_FilmScreening_Error_SalonID(msg)
    

    querry = '''
    select filmscreenings.ShowDate , movies.ShowTime , movies.MovieID
    from filmscreenings
    join movies
    on filmscreenings.MovieID = movies.MovieID
    where filmscreenings.SalonId = %s
    order by filmscreenings.ShowDate 
    '''
    val = (SalonID,)
    Date_and_Time_list = Get_list(querry , val)
    ShowDate = datetime.strptime(ShowDate, '%Y-%m-%d %H:%M:%S')
    res = [True, None]
    for i in range(len(Date_and_Time_list)):
        if Date_and_Time_list[i][0] <= ShowDate < Date_and_Time_list[i][0] + Date_and_Time_list[i][1]:
            res[0] = False
            res[1] = Date_and_Time_list[i][2]
            break
        elif ShowDate < Date_and_Time_list[i][0] < ShowDate + MovieShowTime:
            res[0] = False
            res[1] = Date_and_Time_list[i][2]
            break

    return res