import mysql.connector
from datetime import datetime, timedelta

class Connector_databas:
    def __init__(self):
        self.now = datetime.now()
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
        
    def get_three_result(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0], result[1], result[2] if result else None

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
            return False, "Your Balance is not enough"
        return False, "Your information is incorrect"


   
class Subscription(Connector_databas): 
    def __init__(self):
        self.wallet = Wallet()
        super().__init__()
    def check_expire_date_count(self, user_id):
        query = "SELECT ExpiryDate, Counts, SubscriptionType FROM Subscriptions WHERE UserID = %s"
        expiry_date_count, count, subscription_type = self.get_three_result(query, (user_id,))
        if expiry_date_count:
            today = datetime.now().date()
            if expiry_date_count < today or count == 0:
                query = "DELETE FROM Subscriptions WHERE UserID = %s" 
                self.execute_query(query, (user_id,))
                return False, "Your subscription has expired"
            return True, f"Your subscription has not expired and {count} count is available ", subscription_type, count   
        return False, "Your subscription has expired"
        


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
        result = self.wallet.get_transaction(user_id, cost, f'get {subscription_type}')
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
        new_count = count - 1
        if new_count < 0:
            query = "DELETE FROM Subscriptions WHERE UserID = %s" 
            self.execute_query(query, (user_id,))
            return False, "Your subscription has delete"
            
        elif subscription_type == 'silver':
            new_ticket_price = ticket_price * 0.2
            wallet.back_to_wallet(user_id,new_ticket_price)
        elif subscription_type == 'gold':
            new_ticket_price = ticket_price * 0.5
            wallet.back_to_wallet(user_id,new_ticket_price)
            
            
        query = "UPDATE Subscriptions SET Counts = %s WHERE UserID = %s"
        self.execute_query(query, (new_count, user_id))
        return True, "Your transaction by subscription is successfully."
        
    def view_subscription(self, user_id):
        check_expire = self.check_expire_date_count(user_id)
        if check_expire[0] == True:
            query = "SELECT SubscriptionType FROM Subscriptions WHERE UserID = %s"
            return True, f"Your Subscription Type is {self.get_single_result(query, (user_id,))} and {check_expire[1]}"
        return check_expire[1]
        


class TicketSystem(Connector_databas):   
    def __init__(self):
        self.wallet = Wallet()
        self.subscription = Subscription
        super().__init__()
    def buy_ticket(self, salon_id, user_id, movie_id):
        if check_age_for_ticket(self, user_id, movie_id):
            ticket_price = self.get_single_result("SELECT s.TicketPrice FROM Salons s JOIN Cinemas c ON s.SalonID = c.SalonID WHERE c.MovieID = %s AND c.SalonID = %s", (movie_id, salon_id))
            
            result = self.subscription.check_expire_date_count(user_id)
            if result[0]:                                        
                self.subscription.get_transaction_by_subscription(user_id, result[2], result[3], ticket_price,'buy ticket with subscription')
                get_ticket = self.wallet.get_transaction(user_id, ticket_price, 'get ticket with subscription')
                if get_ticket[0]:
                    return True, "Ticket purchased successfully with subscription !"
                return get_ticket
            get_ticket = self.wallet.get_transaction(user_id, ticket_price, 'get ticket without subscription')
            if get_ticket[0]:
                return True, "Ticket purchased successfully without subscription!"
            return get_ticket
        return False
        
    def age_calculator(self, user_id):
        import datetime
        query = "SELECT Birthday FROM Users WHERE UserID = %s"
        birthdate = self.get_single_result(query, (user_id,))
        birthdate = str(birthdate)
        year,month, day = map(int, birthdate.split("-"))
        today = datetime.date.today()
        age = today.year - year - ((today.month, today.day) < (month, day))
        return age
    def check_age_for_ticket(self, user_id, movie_id):
        age = self.age_calculator(user_id)
        query = "SELECT AgeRating FROM Movies WHERE MovieID = %s"
        age_rating = self.get_single_result(query, (movie_id,))
        if age > age_rating:
            return True
        return False
      




wallet = Wallet()
'''
print(wallet.charge_wallet('3','4444444444444447' ,'Accountspass4','444', 200))   
print(wallet.get_wallet_balance('1'))
'''
# get_transaction
'''
print(wallet.get_transaction('1', 100))
print(wallet.get_wallet_balance('1'))
'''
# get card Balance

#print(wallet.get_card_balance('1'))
# add_card_to_Accounts
'''
print(wallet.add_card_to_Accounts('123456789012870', 'Accountspass1', '111', 500, '1'))
print(wallet.get_card_balance('1'))
'''


s = Subscription()
'''
print(s.update_subscription(1,'silver'))
print(s.view_subscription('1'))
'''


'''
# back_to_wallet
print(wallet.back_to_wallet('1',20))
'''

ticket = TicketSystem()
#print(ticket.buy_ticket('3','1','3'))

print(ticket.check_age_for_ticket('1','1'))

