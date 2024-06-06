import mysql.connector
import getpass

DB_CONFIG = {
    'user': 'your_username',
    'password': 'your_password',
    'host': '127.0.0.1',
    'database': 'cinema',
}
#data base connect
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def comment():
    comment = input("لطفاً کامنت خود را وارد کنید: ")
    sentence = input("لطفاً جمله خود را وارد کنید: ")
    