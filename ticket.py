import mysql.connector

class Wallet:
    def add_bank_account(self, user_id, card_number, password, cvv2, balance):
        query = "INSERT INTO Wallets (CardNumber, WalletPassword, CVV2, Balance, UserID) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (card_number, password, cvv2, balance, user_id))
        self.conn.commit()

    def charge_wallet(self, user_id, amount):
        # self.add_bank_account(user_id, '123456789', 'password123', '123', 0) # Example usage of add_bank_account method
        query = "UPDATE Wallets SET Balance = Balance + %s WHERE UserID = %s"
        self.cursor.execute(query, (amount, user_id))
        self.conn.commit()
    
     
      
    def get_transaction(self, card_number, password, cvv2, amount, info):
            query = "SELECT balance FROM wallet WHERE card_number = %s AND password = %s AND cvv2 = %s"
            self.cursor.execute(query, (card_number, password, cvv2))
            result = self.cursor.fetchone()
            if result:
                balance = result[0]
                if balance >= amount:
                    new_balance = balance - amount
                    query = "UPDATE wallet SET balance = %s WHERE card_number = %s AND password = %s AND cvv2 = %s"
                    self.cursor.execute(query, (new_balance, card_number, password, cvv2))
                    self.conn.commit()
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





