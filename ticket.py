import mysql.connector

class Wallet:
    def get_wallet_balance(self, user_id):
        query = "SELECT Balance FROM Wallets WHERE UserID = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_card_balance(self, card_number):
        query = "SELECT Balance FROM Wallets WHERE CardNumber = %s"
        self.cursor.execute(query, (card_number,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def add_or_subtract_wallet(self, user_id, amount):
        curr_balance = self.get_wallet_balance(user_id)
        if curr_balance is not None:
            new_balance = curr_balance + amount
            query = "UPDATE Wallets SET Balance = %s WHERE UserID = %s"
            self.cursor.execute(query, (new_balance, user_id))
            self.conn.commit()

    def subtract_from_card_balance(self, card_number, amount):
        curr_balance = self.get_card_balance(card_number)
        if curr_balance is not None and curr_balance >= amount:
            new_balance = curr_balance - amount
            query = "UPDATE Wallets SET Balance = %s WHERE CardNumber = %s"
            self.cursor.execute(query, (new_balance, card_number))
            self.conn.commit()

    def add_card_to_wallet(self, user_id, card_number, password, cvv2, balance):
        query = "INSERT INTO Wallets (CardNumber, WalletPassword, CVV2, Balance, UserID) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (card_number, password, cvv2, balance, user_id))
        self.conn.commit()


    def log_transaction(self, card_number, amount, info):
        with open('transaction.log', 'a') as f:
            f.write(f"Card Number: {card_number}\n")
            f.write(f"Amount: {amount}\n")
            f.write(f"Transaction Info: {info}\n")
            f.write("\n")     
      
      
      
      
        
        
class Subscription:
    def __init__(self, subscription_type, expiredate, subscription_info, amount, user_id):
        self.subscription_type = subscription_type
        self.expiredate = expiredate
        self.subscription_info = subscription_info
        self.user_id = user_id
    def get_default(self):
        pass
    def get_silver(self):
        pass
    def get_gold(self):
        pass
    def view_subscription(self):
        print(f"Your Subscription is: {self.type_Subscription}")





