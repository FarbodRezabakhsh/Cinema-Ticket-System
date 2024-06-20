import mysql.connector
from datetime import datetime, timedelta

class Connector_databas:
    def __init__(self):
        self.now = datetime.now()
        self.today = datetime.today()
        self.conn = mysql.connector.connect(
            user='root',
            password='123456789',
            host='localhost',
            database='Ticket'
        )
        self.cursor = self.conn.cursor()
    def get_all_results(self, query, values=None):
        self.cursor.execute(query, values)
        results = self.cursor.fetchall()
        return results if results else None
        
    def get_single_result(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0] if result else None
        
    def get_second_result(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0], result[1] if result else None

    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)
        self.conn.commit()
class Wallet(Connector_databas):  
    def __init__(self):
        super().__init__()
        
    def subtract_from_card_balance(self, user_id, card_number, password, cvv2, amount):
        query = "SELECT CardNumber FROM Accounts WHERE UserID = %s AND CardNumber = %s"
        select_cardnumber = self.get_single_result(query, (user_id, card_number))
        if select_cardnumber is not None:
            query = "SELECT Amount FROM Accounts WHERE UserID = %s AND CardNumber = %s AND AccountPassword = %s AND CVV2 = %s"
            curr_balance = self.get_single_result(query, (user_id, card_number, password, cvv2))
            if curr_balance is not None:
                if curr_balance >= amount:
                    new_balance = curr_balance - amount
                    query = "UPDATE Accounts SET Amount = %s WHERE CardNumber = %s"
                    self.execute_query(query, (new_balance, card_number))
                    self.log_transaction(user_id, amount, 'subtract from card balance')
                    return True, "Transaction is complete. Your balance has been updated."
                return False, "Your Balance card number is not enough"
            return False, "Your information is incorrect"
        return False, "Your card number incorrect !!"
        
    def back_to_wallet(self, user_id, amount):
        query = "SELECT Balance FROM Wallets WHERE UserID = %s"
        curr_balance = self.get_single_result(query, (user_id,))
        new_balance = curr_balance+ amount
        query = "UPDATE Wallets SET Balance = %s WHERE UserID = %s"
        self.execute_query(query, (new_balance, user_id))
        self.log_transaction(user_id, amount, 'back amount to wallet')
        return True, "Back amount to wallet was successfully."
        
        
        
    def charge_wallet(self, user_id, card_number, password, cvv2, amount):
        result = self.subtract_from_card_balance(user_id, card_number, password, cvv2, amount)
        if result[0]:
            query = "SELECT Balance FROM Wallets WHERE UserID = %s"
            curr_balance = self.get_single_result(query, (user_id,))
            if curr_balance is not None:
                new_balance = curr_balance+ amount
                query = "UPDATE Wallets SET Balance = %s WHERE UserID = %s"
                self.execute_query(query, (new_balance, user_id))
                self.log_transaction(user_id, amount, 'charge wallet')
                return True, "Your balance Wallet has been updated successfully."
            query = "INSERT INTO Wallets (UserID, Balance) VALUES (%s, %s)"
            self.execute_query(query, (user_id, amount))
            return True, "Your Wallets has been Create successfully."
        elif result[0] == False:
            return result
        return False, "Transaction dose not complete."

    def add_card_to_Accounts(self, card_number, password, cvv2, amount, user_id):
        query_getcard = "SELECT CardNumber FROM Accounts WHERE CardNumber = %s"
        existing_card = self.get_single_result(query_getcard, (card_number,))
        if existing_card == card_number:
            query_get_balance = "SELECT Amount FROM Accounts WHERE UserID = %s AND CardNumber = %s"
            curr_balance = self.get_single_result(query_get_balance, (user_id, card_number))
            new_balance = curr_balance + amount
            query = "UPDATE Accounts SET Amount = %s WHERE UserID = %s AND CardNumber = %s"
            self.execute_query(query, (new_balance, user_id, card_number))
            return True, "Amount The card number has been updated."
        
        query = "INSERT INTO Accounts (CardNumber, AccountPassword, CVV2, Amount, UserID) VALUES (%s, %s, %s, %s, %s)"
        self.execute_query(query, (card_number, password, cvv2, amount, user_id))
        return True, "Your card has been added to your account."


    def get_wallet_balance(self, user_id):
        query = "SELECT Balance FROM Wallets WHERE UserID = %s"
        result = self.get_single_result(query, (user_id,)) 
        if result is not None:
            return result
        return False, "The user either does not have a wallet set up or has selected the wrong user. Please try again."
    
    def get_card_balance(self, user_id):
        query = "SELECT Amount, CardNumber FROM Accounts WHERE UserID = %s"
        results = self.get_all_results(query, (user_id,))
        if results:
            for result in results:
                print(f"Card number {result[1]} is {result[0]} Amount")
            return True
        return False, "You have selected the wrong user. I am unable to find him."

    def log_transaction(self, user_or_card_info, amount, info):
        with open('transaction.log', 'a') as f:
            f.write(f"User ID: {user_or_card_info}, Amount: {amount}, Transaction Info: {info}, \n")
    
    def get_transaction(self, user_id, amount, info='get ticket or Subscription'):
        query = "SELECT Balance FROM Wallets WHERE UserID = %s"
        curr_balance = self.get_single_result(query, (user_id,))
        if curr_balance is not None:
            if curr_balance >= amount:
                new_balance = curr_balance - amount
                query = "UPDATE Wallets SET Balance = %s WHERE UserID = %s"
                self.execute_query(query, (new_balance, user_id))
                self.log_transaction(user_id, amount, info)
                return True, "Transaction is complete."
            return False, "Wallet balance is not enough."
        return False, "You do not have a wallet, please charge your wallet"
    def create_wallet(self, user_id):
        query = "SELECT Balance FROM Wallets WHERE UserID = %s"
        curr_balance = self.get_single_result(query, (user_id,))
        if curr_balance is None:
            balance = 0
            query = "INSERT INTO Wallets (Balance, UserID) VALUES (%s, %s)"
            self.execute_query(query, (balance, user_id))
            return True,"Your wallet is create."
        return False, "This user is have a wallet. you can not create again." 
        

   
class Subscription(Wallet): 
    def __init__(self):
   
        super().__init__()
    def check_expire_date_count(self, user_id):
        query = "SELECT SubscriptionType FROM Subscriptions WHERE UserID = %s"
        subscription_type = self.get_single_result(query, (user_id,))
        if subscription_type is not None:
            query = "SELECT ExpiryDate FROM Subscriptions WHERE UserID = %s"
            expiry_date_count = self.get_single_result(query, (user_id,))
            
            query = "SELECT Counts FROM Subscriptions WHERE UserID = %s"
            count = self.get_single_result(query, (user_id,))
            
            if expiry_date_count:
                today = datetime.now().date()
                if expiry_date_count < today or count == 0:
                    query = "DELETE FROM Subscriptions WHERE UserID = %s" 
                    self.execute_query(query, (user_id,))
                    return False, "Your subscription has expired"
                return True, f"Your subscription has not expired and {count} count is available ", subscription_type, count   
            return False, "Your subscription has expired"
        return False, "Unfortunately, you do not have a subscription."
        


    def check_subscription_type(self, subscription_type):
        if subscription_type == 'silver':
            cost = 100 
            expire_days = 90
            subscription_info = 'Basic'
            counts = 3
        elif subscription_type == 'gold': 
            cost = 200
            expire_days = 180
            subscription_info = 'Premium'
            counts = 5
        return cost, expire_days, subscription_info, counts

    
    def update_subscription(self, user_id, subscription_type):
        cost, expire_days, subscription_info, counts = self.check_subscription_type(subscription_type)
        expire_date = self.now + timedelta(days=expire_days)
        query = "SELECT SubscriptionType FROM Subscriptions WHERE UserID = %s"
        curr_subscription = self.get_single_result(query, (user_id,))
        result = self.get_transaction(user_id, cost, f'get {subscription_type}')
        if curr_subscription and result[0]:
            query = "UPDATE Subscriptions SET SubscriptionType = %s, ExpiryDate = %s, SubscriptionInfo = %s, Counts = %s WHERE UserID = %s"
            self.execute_query(query, (subscription_type, expire_date, subscription_info, counts, user_id))
            return True, "Your subscription is update."
        elif result[0] == False:
            return result
        else:
            query = "INSERT INTO Subscriptions (UserID, SubscriptionType, ExpiryDate, SubscriptionInfo, Counts) VALUES (%s, %s, %s, %s, %s)"
            self.execute_query(query, (user_id, subscription_type, expire_date, subscription_info, counts))
            return True, "The subscription transaction  was completed successfully"
        
        
    def get_transaction_by_subscription(self, user_id, subscription_type, count, ticket_price):
        if count == 0 :
            query = "DELETE FROM Subscriptions WHERE UserID = %s" 
            self.execute_query(query, (user_id,))
            return False, "Your subscription has delete"
            
        elif subscription_type == 'silver':
            new_ticket_price = ticket_price * 0.2
            self.back_to_wallet(user_id,new_ticket_price)
        elif subscription_type == 'gold':
            new_ticket_price = ticket_price * 0.5
            self.back_to_wallet(user_id,new_ticket_price)
        count = count - 1
            
            
        query = "UPDATE Subscriptions SET Counts = %s WHERE UserID = %s"
        self.execute_query(query, (count, user_id))
        return True, "Your transaction by subscription is successfully.", new_ticket_price
        
    def view_subscription(self, user_id):
        check_expire = self.check_expire_date_count(user_id)
        if check_expire[0] == True:
            query = "SELECT SubscriptionType FROM Subscriptions WHERE UserID = %s"
            return True, f"Your Subscription Type is {self.get_single_result(query, (user_id,))} and {check_expire[1]}"
        return check_expire[1]
        


class TicketSystem(Subscription):   
    def __init__(self):
        super().__init__()
        
    def buy_ticket(self, user_id, salon_id, movie_id):
        if self.check_age_for_ticket(user_id, movie_id):
            query = "SELECT s.TicketPrice FROM Salons s JOIN Cinemas c ON s.SalonID = c.SalonID WHERE c.MovieID = %s AND c.SalonID = %s"
            ticket_price = self.get_single_result(query, (salon_id,movie_id))
            check_birthdate = self.age_calculator(user_id)
            if check_birthdate[0]:
                ticket_price//=2
            result = self.check_expire_date_count(user_id)
            if result[0]:                                        
                new_price = self.get_transaction_by_subscription(user_id, result[2], result[3], ticket_price)
                get_ticket = self.get_transaction(user_id, ticket_price, 'get ticket with subscription')
                if get_ticket[0]:
                    new_ticket = ticket_price - new_price[2]
                    self.get_ticket(user_id, salon_id, movie_id, new_ticket)
                    return True, "Ticket purchased successfully with subscription !"
                return get_ticket
            get_ticket = self.get_transaction(user_id, ticket_price, 'get ticket without subscription')
            if get_ticket[0]:
                if self.get_ticket(user_id, salon_id, movie_id, ticket_price):
                    return True, "Ticket purchased successfully without subscription!"
            return get_ticket
        return False ,"Your age is too young to see this file"
        
    def age_calculator(self, user_id):
        import datetime
        query = "SELECT Birthday FROM Users WHERE UserID = %s"
        birthdate = self.get_single_result(query, (user_id,))
        birthdate = str(birthdate)
        year,month, day = map(int, birthdate.split("-"))
        today = datetime.date.today()
        age = today.year - year - ((today.month, today.day) < (month, day))
        if day == today.day and month == today.month:
            return True, age
        return False, age
    def check_age_for_ticket(self, user_id, movie_id):
        age = self.age_calculator(user_id)
        query = "SELECT AgeRating FROM Movies WHERE MovieID = %s"
        age_rating = self.get_single_result(query, (movie_id,))
        if age[1] > age_rating:
            return True
        return False
      
    def get_ticket(self, user_id, salon_id, movie_id, ticket_price):
        seat_row = 1
        seat_column = 1
        query = "INSERT INTO Tickets (UserID, SalonID, MovieID, SeatRow, SeatColumn, TicketPrice) VALUES (%s, %s, %s, %s, %s, %s)"
        self.execute_query(query, (user_id, salon_id, movie_id, seat_row, seat_column, ticket_price))
        return True , "Your ticket is compleate"

    def cancel_ticket(self, ticket_id):
        query = "SELECT MovieID, UserID, TicketPrice FROM Tickets WHERE TicketID = %s"
        movie_id = self.get_single_result(query, (ticket_id,))
        if self.check_time_ticket(ticket_id, movie_id):
            query = "SELECT UserID, TicketPrice FROM Tickets WHERE TicketID = %s"
            user_id, ticketprice = self.get_second_result(query, (ticket_id,))
            self.back_to_wallet(user_id, ticketprice)
            query = "DELETE FROM Tickets WHERE TicketID = %s" 
            self.execute_query(query, (ticket_id,))
            return True ,"your ticket is delete and price get to your wallet"
        return False, "Your ticket has expired. You can not cancel it."
        
    def check_time_ticket(self, ticket_id, movie_id):
        import datetime
      #  today_time = self.today
        query = "SELECT M.ShowTime FROM Tickets T JOIN Movies M ON T.MovieID = M.MovieID WHERE T.TicketID = %s AND T.MovieID = %s"
        ticket_time = self.get_single_result(query, (ticket_id, movie_id))
        query = "SELECT C.ShowDate FROM Tickets T JOIN Cinemas C ON T.MovieID = C.MovieID AND T.SalonID = C.SalonID WHERE T.TicketID = %s AND T.MovieID = %s"
        ticket_date = self.get_single_result(query, (ticket_id, movie_id))
        t = f"{ticket_date} {ticket_time}"
        ticket_datetime = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        if self.today.now() > ticket_datetime:
            return False
        return True




     
                
ticket = TicketSystem()

# add_card_to_Accounts
'''
#print(ticket.add_card_to_Accounts('8888888888888888', 'Accountspass8', '888', 500, 1))
print(ticket.get_card_balance(1))
'''

#print(ticket.charge_wallet(1,'8888888888888888' ,'Accountspass8','888', 500))   
#print(ticket.get_wallet_balance('1'))

# get_transaction

#print(ticket.get_transaction(3, 1000))
#print(ticket.get_wallet_balance(3))

# get card Balance

#print(ticket.get_card_balance(8))





#print(ticket.update_subscription(1,'gold'))


#print(ticket.view_subscription(1))




# back_to_wallet
'''
print(ticket.back_to_wallet(1,20))
'''
# get ticket


#print(ticket.buy_ticket(1,'3','3'))

#print(ticket.check_age_for_ticket(1,'1'))


#print(ticket.cancel_ticket(10))


#print(ticket.age_calculator(1))

#print(ticket.check_time_ticket(1,3))

print(ticket.create_wallet(3))
