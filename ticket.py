import mysql.connector
from datetime import datetime, timedelta

class Wallet: 
    def __init__(self):
        self.conn = mysql.connector.connect(
            user='root',
            password='123456789',
            host='localhost',
            database='Ticket'
        )
        self.cursor = self.conn.cursor()

    def get_single_result(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)
        self.conn.commit()

    def subtract_from_card_balance(self, user_id, card_number, password, cvv2, amount):
        query = "SELECT Amount FROM Accounts WHERE UserID = %s AND CardNumber = %s AND AccountPassword = %s AND CVV2 = %s"
        curr_balance = self.get_single_result(query, (user_id, card_number, password, cvv2))
        if curr_balance is not None:
            if curr_balance >= amount:
                new_balance = curr_balance - amount
                query = "UPDATE Accounts SET Amount = %s WHERE CardNumber = %s"
                self.execute_query(query, (new_balance, card_number))
                self.log_transaction(user_id, amount, 'subtract_from_card_balance')
                return True, "Transaction is complete. Your balance has been updated."
            return False, "Your Balance is not enough"
        return False, "Your information is incorrect"
    
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
                return True, "Transaction is complete. Your Charge Wallet has been updated."
            query = "INSERT INTO Wallets (UserID, Balance) VALUES (%s, %s)"
            self.execute_query(query, (user_id, amount))
            return True, "Transaction is complete. Your balance has been updated."
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
            return True, "Amount card number is update."
        
        query = "INSERT INTO Accounts (CardNumber, AccountPassword, CVV2, Amount, UserID) VALUES (%s, %s, %s, %s, %s)"
        self.execute_query(query, (card_number, password, cvv2, amount, user_id))
        return True, "Your card is add to your account."


    def get_wallet_balance(self, user_id):
        query = "SELECT Balance FROM Wallets WHERE UserID = %s"
        result = self.get_single_result(query, (user_id,)) 
        if result is not None:
            return result
        return False, "Your information is incorrect"

    
    def get_card_balance(self, user_id):
        query = "SELECT SUM(Amount) FROM Accounts WHERE UserID = %s"
        result = self.get_single_result(query, (user_id,))
        if result:
            return result
        return False, "Your information is incorrect"

    def log_transaction(self, user_or_card_info, amount, info):
        with open('transaction.log', 'a') as f:
            f.write(f"User ID: {user_or_card_info} Amount: {amount} Transaction Info: {info} \n")

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


   
class Subscription: 
    def __init__(self): 
        self.conn = mysql.connector.connect(
            user='root',
            password='123456789',
            host='localhost',
            database='Ticket'
        )
        self.cursor = self.conn.cursor()
        self.now = datetime.now()
        self.wallet = Wallet()
    def get_single_result(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result[0] if result else None

    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)
        self.conn.commit()
        
    def check_expire_date(self, user_id):
        query = "SELECT ExpiryDate FROM Subscriptions WHERE UserID = %s"
        curr_subscription = self.get_single_result(query, (user_id,))
        print(curr_subscription)   
        
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
        
        
        

    def view_subscription(self, user_id):
        query = "SELECT SubscriptionType FROM Subscriptions WHERE UserID = %s"
        return self.get_single_result(query, (user_id,))
        
        
wallet = Wallet()

# charge_wallet
'''
print(wallet.charge_wallet('1','123456557890128745' ,'Accountspass1','111', 200))   
print(wallet.get_wallet_balance('1'))
'''
# get_transaction

'''
print(wallet.get_transaction('1', 10000))
print(wallet.get_wallet_balance('1'))
'''

# add_card_to_Accounts
'''
print(wallet.add_card_to_Accounts('1234567890128845', 'Accountspass1', '111', 900.00, '1'))
print(wallet.get_card_balance('1'))
'''


s = Subscription()
print(s.update_subscription(1,'gold'))
#print(s.view_subscription('1'))
 
        


