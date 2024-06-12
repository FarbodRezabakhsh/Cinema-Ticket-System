from ErrorHandeling import *
from sql_connecter import *

def Delete_Movie_Handler(MovieID : int):
    querry = '''
            select movies.MovieID
            from movies
            where movies.MovieID = %s
            '''
    val = (MovieID, )
    IDs = Get_list(querry, val)
    if IDs == []:
        msg = "There isn't any Movie with MovieID : {}".format(MovieID)
        raise Delete_Movie(msg)


    querry = '''
            select movies.MovieID , filmscreenings.filmscreeningID
            from movies
            join filmscreenings
            on movies.MovieID = filmscreenings.MovieID
            where movies.MovieID = %s
            '''
    val = (MovieID, )
    IDs = Get_list(querry, val)
    res = []
    for MovieID , FilmScreeningID in IDs:
        res += Delete_FilmScreening_Handler(FilmScreeningID)

    return res


def Delete_Salon_Handler(SalonID : int):
    querry = '''
            select salons.SalonID
            from Salons
            where salons.SalonID = %s
            '''
    val = (SalonID, )
    IDs = Get_list(querry, val)
    if IDs == []:
        msg = "There isn't any Salon with SalonID : {}".format(SalonID)
        raise Delete_Salon(msg)


    querry = '''
            select salons.SalonID , filmscreenings.filmscreeningID
            from salons
            join filmscreenings
            on salons.SalonID = filmscreenings.SalonID
            where salons.SalonID = %s
            '''
    val = (SalonID, )
    IDs = Get_list(querry, val)
    res = []
    for SalonID , FilmScreeningID in IDs:
        res += Delete_FilmScreening_Handler(FilmScreeningID)
    return res


def Delete_FilmScreening_Handler(FilmScreeningID : int):
    querry = '''
            select FilmScreenings.FilmScreeningID
            from FilmScreenings
            where FilmScreenings.FilmScreeningID = %s
            '''
    val = (FilmScreeningID, )
    IDs = Get_list(querry, val)
    if IDs == []:
        msg = "There isn't any FilmScreening with FilmScreeningID : {}".format(FilmScreeningID)
        raise Delete_FilmScreening(msg)


    querry = '''
            select wallets.WalletID , tickets.TicketPrice , Wallets.Balance , users.UserID
            from tickets
            join filmscreenings
            on tickets.FilmScreeningID = filmscreenings.FilmScreeningID
            JOIN users
            on tickets.UserID = users.UserID
            join wallets
            on users.WalletID = wallets.WalletID
            where filmscreenings.FilmScreeningID = %s
            '''
    val = (FilmScreeningID, )
    IDs_Prices = Get_list(querry, val)

    res = []

    querry = '''
        UPDATE wallets
        SET Balance = %s
        where WalletID = %s
        '''
    for WalletID , TicketPrice , Balance , UserID in IDs_Prices:
        val = (TicketPrice + Balance , WalletID)
        Exe(querry, val)
        res.append("TicketPrice {} added to WalletID {} belong to UserID {}." .format(TicketPrice , WalletID , UserID))
    
    return res