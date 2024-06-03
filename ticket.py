class Wallet:
    def __init__(self,user_id):
        self.user_id = user_id
        self.bank_accounts = []
        self.wallet_balance = 0
    
    def add_bank_account(self,  card_number, password, ccv, balance):
        bank_account = {
        "card_number" : card_number,
        "password" : password,
        "ccv" : ccv,
        "balance" : balance,
        }
        
        self.bank_accounts.append(bank_account)
    def view_bank_accounts(self,user_id):
        for i, account in enumerate(self.bank_accounts):
            print(f"Bank Account {i+1}:")
            print(f"Card Number: {account['card_number']}")
            print(f"Balance: {account['balance']}")
            
    def charge_wallet(self, card_number, amount):
        for account in self.bank_accounts:
            if card_number == account['card_number']:
                account["balance"]+= amount
                print(f"Current balance in Bank Account {account['card_number']} is {account['balance']}")
            else:
                print("Invalid account index.")
            
    def view_wallet_balance(self):
        print(f"Current balance in wallet: {self.wallet_balance}")
        
    
    def buy_ticket(self, ticket_price):
        if ticket_price <= self.wallet_balance:
            self.wallet_balance -= ticket_price
            print("Ticket purchased successfully!")
        else:
            print("Insufficient balance in wallet.")


        
        
        
        
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


class Cinema_ticket:
    def __init__(self,info):
        self.wallet = Wallet("1234 5678 9012 3456", "password123", "123", 100, "user123")
        self.info = info
    
    def buy_ticket(self, ticket_price):
        if ticket_price <= self.wallet.balance:
            self.wallet.balance -= ticket_price
            print("Ticket purchased successfully!")
        else:
            print("Insufficient balance in wallet.")




if __name__ == "__main__":
    test = Wallet(1)
    test.add_bank_account(5022291087043244,123456,123,50000)
    test.view_bank_accounts()
    test.charge_wallet(5022291087043244,50000)
    test.view_bank_accounts()
