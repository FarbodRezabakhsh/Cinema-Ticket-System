import os
from AdminClass import *

os.system("cls||clear")

myAdmin = Admin(1)

class AdminMenu:
    def AdminPage(self):
        print('''
            **Admin page**
            Enter  <1>  for  [Show All Movies]
            Enter  <2>  for  [Show All Salons]
            Enter  <3>  for  [Show All FilmScreenins]
            Enter  <4>  for  [Define new Movie]
            Enter  <5>  for  [Define new Salon]
            Enter  <6>  for  [Define new FilmScreening]
            Enter  <7>  for  [Delete old movie]
            Enter  <8>  for  [Delete old Salon]
            Enter  <9>  for  [Delete old FilmScreening]
            Enter  <0>  for  [Back]
            ''')
        order = input()
        os.system("cls||clear")

        if order == "1":
            all = myAdmin.Get_All_Movies()

            for i in all:
                print(*i)
            return self.AdminPage()

        elif order == "2":
            all = myAdmin.Get_All_Salons()
            for i in all:
                print(*i)
            return self.AdminPage()
            
        elif order == "3":
            all = myAdmin.Get_All_FilmScreenings()
            for i in all:
                print(*i)
            return self.AdminPage()
            
        elif order == "4":
            print("Enter MovieName: ")
            MovieName = input()
            print("Enter AgeRating: ")
            AgeRating = int(input())
            print("Enter ShowTime: ") 
            ShowTime = input()
            myAdmin.Define_Movie(MovieName, AgeRating, ShowTime)
            os.system("cls||clear")
            print("MovieName {} with AgeRating {} and ShowTime {} is added to Movie Table".format(MovieName, AgeRating, ShowTime))
            return self.AdminPage()

        elif order == "5":
            print("Enter RowCount: ")
            RowCount = int(input())
            print("Enter ColumnCount: ")
            ColumnCount = int(input())
            print("Enter TicketPrice: ") 
            TicketPrice = float(input())
            myAdmin.Define_Salon(RowCount, ColumnCount, TicketPrice)
            os.system("cls||clear")
            print("Salon with RowCount {} and ColumnCount {} and TicketPrice {} is added to Salon Table".format(RowCount, ColumnCount, TicketPrice))
            return self.AdminPage()
        
        elif order == "6":
            print("Enter MovieID: ")
            MovieID = int(input())
            print("Enter SalonID: ")
            SalonID = int(input())
            print("Enter ShowDate: ") 
            ShowDate = input()
            os.system("cls||clear")
            msg = myAdmin.Define_FilmScreening(MovieID, SalonID, ShowDate)
            if msg != None :
                print(msg)
            else:
                print("FilmScreening with MovieID {} and SalonID {} and ShowDate {} is added to FilmScreening Table".format(MovieID, SalonID, ShowDate))
            return self.AdminPage()
        
        elif order == "7":
            print("Enter MovieID: ")
            MovieID = int(input())
            print(myAdmin.Delete_Movie(MovieID))
            return self.AdminPage()
        
        elif order == "8":
            print("Enter SalonID: ")
            SalonID = int(input())
            print(myAdmin.Delete_Salon(SalonID))
            return self.AdminPage()
           
        elif order == "9":
            print("Enter FilmScreeningID: ")
            FilmScreeningID = int(input())
            print(myAdmin.Delete_FilmScreening(FilmScreeningID))
            return self.AdminPage()
        
        elif order == "0":
            pass

        else:
            os.system("cls||clear")
            print("Input is incorrect. Try again!")
            return self.AdminPage()


myStart = AdminMenu()
myStart.AdminPage()