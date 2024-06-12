from sql_connecter import *
from DeletingHandeling import *

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
        res = Delete_Salon_Handler(self.SalonID)
        querry = '''DELETE FROM Salons
                    WHERE SalonID = %s'''
        val = (self.SalonID, )
        Exe(querry , val)
        return res 

    def Get_All_Salons():
        '''
        Return All Salons from Salons table.
        '''    
        querry = ('''SELECT *
                    FROM Salons''')
        return Get(querry)
    
    
