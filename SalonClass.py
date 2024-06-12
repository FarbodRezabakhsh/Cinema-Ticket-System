from sql_connecter import *

class Salon:
    '''    
    A class to represent Salon.
    '''
    def __init__(self, SalonID : int, RowCount : int, ColumnCount : int, TicketPrice : float):
        '''
        Constructs:
        SalonID : int 
        RowCount : int
        ColumnCount : int
        TicketPrice : float
        '''
        self.SalonID = SalonID
        self.RowCount = RowCount
        self.ColumnCount = ColumnCount
        self.TicketPrice = TicketPrice
    
    def Define_Salon(self):
        '''
        Insert Into Salons Table New_Salon
        '''
        querry = '''INSERT INTO Salons(RowCount, ColumnCount, TicketPrice)
                    VALUES (%s, %s, %s)''' 
        val = (self.RowCount, self.ColumnCount, self.TicketPrice)
        Exe(querry, val)

    def Delete_Salon(self):
        '''
        Delete from Salons Table Old_Salon
        '''
        querry = '''DELETE FROM Salons
                    WHERE SalonID = %s'''
        val = (self.SalonID, )
        Exe(querry , val)
    
    def Salon_Situation(self):
        '''
        Return Matrix of Salin seat situation.
        '''
        querry = ('''Select SeatRow , SeatColumn
                    from tickets
                    join filmscreenings
                    on filmscreenings.FilmScreeningID = tickets.FilmScreeningID
                    join salons
                    on filmscreenings.SalonID = salons.SalonID
                    Where salons.SalonID = %s ''')
        val = (self.SalonID , )
        return Get_list(querry, val)

    def Get_All_Salons():
        '''
        Return All Salons from Salons table.
        '''    
        querry = ('''SELECT *
                    FROM Salons''')
        return Get(querry)
    
    
