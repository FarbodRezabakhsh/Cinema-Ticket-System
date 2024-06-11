import mysql.connector
from datetime import datetime

class Wallet: 
    def init(self, cursor, conn): 
        self.cursor = cursor 
        self.conn = conn
    
    def get_single_result(self, query, values=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
            result = cursor.fetchone()
        return result[0] if result else None
    
    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)
        self.conn.commit()


    def charge_wallet(self, user_id, amount):
        query = "SELECT Balance FROM Wallets WHERE UserID = %s"
        curr_balance = self.get_single_result(query, (user_id,))
        if curr_balance is not None:
            new_balance = curr_balance + amount
            query = "UPDATE Wallets SET Balance = %s WHERE UserID = %s"
            self.execute_query(query, (new_balance, user_id))
            self.log_transaction(user_id, amount, 'charge wallet')
            return True
        return False

    def subtract_from_card_balance(self, card_number, amount):
        curr_balance = self.get_card_balance(card_number)
        if curr_balance is not None and curr_balance >= amount:
            new_balance = curr_balance - amount
            query = "UPDATE Wallets SET Balance = %s WHERE CardNumber = %s"
            self.execute_query(query, (new_balance, card_number))
            self.log_transaction(card_number, amount, 'subtract_from_card_balance')

    def add_card_to_wallet(self, user_id, card_number, password, cvv2, balance):
        query = "INSERT INTO Wallets (CardNumber, WalletPassword, CVV2, Balance, UserID) VALUES (%s, %s, %s, %s, %s)"
        self.execute_query(query, (card_number, password, cvv2, balance, user_id))

    def get_wallet_balance(self, user_id):
        query = "SELECT Balance FROM Wallets WHERE UserID = %s"
        return self.get_single_result(query, (user_id,))

    def get_card_balance(self, card_number):
        query = "SELECT Balance FROM Wallets WHERE CardNumber = %s"
        return self.get_single_result(query, (card_number,))

    def log_transaction(self, user_or_card_info, amount, info):
        with open('transaction.log', 'a') as f:
            f.write(f"Card Number: {user_or_card_info}\n")
            f.write(f"Amount: {amount}\n")
            f.write(f"Transaction Info: {info}\n")
            f.write("\n")

    def get_transaction(self, card_number, password, cvv2, amount, info='get ticket'):
        query = "SELECT Balance FROM Wallets WHERE CardNumber = %s AND WalletPassword = %s AND CVV2 = %s"
        curr_balance = self.get_single_result(query, (card_number, password, cvv2))
        if curr_balance is not None and curr_balance >= amount:
            new_balance = curr_balance - amount
            query = "UPDATE Wallets SET Balance = %s WHERE CardNumber = %s AND WalletPassword = %s AND CVV2 = %s"
            self.execute_query(query, (new_balance, card_number, password, cvv2))
            self.log_transaction(card_number, amount, info)

        
    def get_subscription(self, user_id, amount, info='get Subscription'):
        query = "SELECT Balance FROM Wallets WHERE UserID = %s"
        curr_balance = self.get_single_result(query, (user_id,))
        if curr_balance is not None and curr_balance >= amount:
            new_balance = curr_balance - amount
            query = "UPDATE Wallets SET Balance = %s WHERE UserID = %s"
            self.execute_query(query, (new_balance,))
            self.log_transaction(user_id, amount, info)
    

class Subscription: 
    def init(self, cursor, conn): 
        self.cursor = cursor
        self.conn = conn 
        self.now = datetime.now()

    def execute_query(self, query, values=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
        self.conn.commit()

    def get_single_result(self, query, values=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
            result = cursor.fetchone()
        return result[0] if result else None

    def update_subscription(self, user_id, subscription_type, expire_days):
        wallet = Wallet(self.cursor, self.conn)
        if subscription_type == 'silver':
            cost = 100 
        elif subscription_type == 'gold': 
            cost = 200
        wallet.get_subscription(user_id, cost, f'get {subscription_type}')
        expiredate = self.now + timedelta(days=expire_days)
        query = "UPDATE Subscription SET Subscription_type = %s, Expiredate = %s WHERE UserID = %s"
        self.execute_query(query, (subscription_type, expiredate, user_id))

    def get_silver(self, user_id):
        self.update_subscription(user_id, 'silver', 90)

    def get_gold(self, user_id):
        self.update_subscription(user_id, 'gold', 150)

    def view_subscription(self, user_id):
        query = "SELECT subscription_type FROM Subscription WHERE UserID = %s"
        return self.get_single_result(query, (user_id,))
