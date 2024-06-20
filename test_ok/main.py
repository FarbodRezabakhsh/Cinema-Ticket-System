import sqlite3
import hashlib
import getpass
import os
from datetime import datetime


class Database:
    @staticmethod
    def connect():
        return sqlite3.connect('cinema_ticket.db')

    @staticmethod
    def execute(query, params=None):
        if params is None:
            params = ()
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    @staticmethod
    def fetch(query, params=None):
        if params is None:
            params = ()
        conn = Database.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results


class User:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def register():
        User.clear_screen()
        username = input("نام کاربری را وارد کنید: ")
        password = input("رمز عبور را وارد کنید: ")
        email = input("ایمیل را وارد کنید: ")
        phone = input("شماره تلفن را وارد کنید: ")
        birth_date = input("تاریخ تولد را وارد کنید (YYYY-MM-DD): ")
        try:
            User.execute_query_register(username, User.hash_password(password), email, phone, birth_date)
            print("ثبت نام با موفقیت انجام شد")
        except Exception as e:
            print(f"خطا: {e}")

    @staticmethod
    def login():
        User.clear_screen()
        username = input("نام کاربری را وارد کنید: ")
        password = input("رمز عبور را وارد کنید: ")
        user = User.execute_query_login(username, User.hash_password(password))
        if user:
            print("ورود با موفقیت انجام شد")
            return user[0], user[1]
        else:
            print("اعتبارنامه نادرست")
            return None, None

    @staticmethod
    def execute_query_register(username, password, email, phone, birth_date):
        query = '''
        INSERT INTO Users (UserID, Password, Name, PhoneNumber, Email, Birthday, RegistrationMonthYear, RegistrationDate, WalletID, SubscriptionID, IsAdmin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        registration_month_year = datetime.now().strftime('%Y-%m')
        registration_date = datetime.now().strftime('%Y-%m-%d')
        params = (
        username, password, username, phone, email, birth_date, registration_month_year, registration_date, None, None,
        False)
        Database.execute(query, params)

    @staticmethod
    def execute_query_login(username, password):
        query = '''
        SELECT UserID, IsAdmin FROM Users
        WHERE UserID = ? AND Password = ?
        '''
        params = (username, password)
        result = Database.fetch(query, params)
        return result[0] if result else None


class Admin:
    @staticmethod
    def add_movie():
        User.clear_screen()
        title = input("عنوان فیلم را وارد کنید: ")
        description = input("توضیحات فیلم را وارد کنید: ")
        release_date = input("تاریخ اکران را وارد کنید (YYYY-MM-DD): ")
        cinema_id = input("شناسه سینما را وارد کنید: ")
        try:
            Admin.execute_query_add_movie(title, description, release_date, cinema_id)
            print("فیلم با موفقیت اضافه شد")
        except Exception as e:
            print(f"خطا: {e}")

    @staticmethod
    def delete_movie():
        User.clear_screen()
        movie_id = input("شناسه فیلم برای حذف را وارد کنید: ")
        try:
            Admin.execute_query_delete_movie(movie_id)
            print("فیلم با موفقیت حذف شد")
        except Exception as e:
            print(f"خطا: {e}")

    @staticmethod
    def execute_query_add_movie(title, description, release_date, cinema_id):
        query = '''
        INSERT INTO Movies (MovieName, Description, ReleaseDate, CinemaID)
        VALUES (?, ?, ?, ?)
        '''
        params = (title, description, release_date, cinema_id)
        Database.execute(query, params)

    @staticmethod
    def execute_query_delete_movie(movie_id):
        query = '''
        DELETE FROM Movies WHERE MovieID = ?
        '''
        params = (movie_id,)
        Database.execute(query, params)


class Menu:
    @staticmethod
    def add_comment(user_id):
        User.clear_screen()
        comment_text = input("نظر خود را وارد کنید: ")
        movie_id = int(input("شناسه فیلم را وارد کنید: "))
        release_date = datetime.now().strftime('%Y-%m-%d')
        reply = input("پاسخ (در صورت وجود) را وارد کنید: ")
        try:
            query = '''
            INSERT INTO Comments (CommentText, UserID, MovieID, CommentDate, ReplyText)
            VALUES (?, ?, ?, ?, ?)
            '''
            params = (comment_text, user_id, movie_id, release_date, reply)
            Database.execute(query, params)
            print("نظر با موفقیت اضافه شد")
        except Exception as e:
            print(f"خطا: {e}")

    @staticmethod
    def delete_comment():
        User.clear_screen()
        comment_id = int(input("شناسه نظر برای حذف را وارد کنید: "))
        try:
            query = '''
            DELETE FROM Comments WHERE CommentID = ?
            '''
            params = (comment_id,)
            Database.execute(query, params)
            print("نظر با موفقیت حذف شد")
        except Exception as e:
            print(f"خطا: {e}")

    @staticmethod
    def user_menu(user_id):
        while True:
            User.clear_screen()
            print("\nمنوی کاربر")
            print("1. انتخاب سالن و فیلم")
            print("2. خرید بلیط")
            print("3. خرید اشتراک")
            print("4. اضافه کردن نظر")
            print("5. حذف نظر")
            print("6. خروج")
            choice = input("انتخاب خود را وارد کنید: ")
            if choice == '1':
                Menu.select_salone_and_movie(user_id)
            elif choice == '2':
                Menu.buy_ticket(user_id)
            elif choice == '3':
                Menu.buy_subscription(user_id)
            elif choice == '4':
                Menu.add_comment(user_id)
            elif choice == '5':
                Menu.delete_comment()
            elif choice == '6':
                break
            else:
                print("انتخاب نامعتبر")

    @staticmethod
    def admin_menu():
        while True:
            User.clear_screen()
            print("\nمنوی مدیر")
            print("1. اضافه کردن فیلم")
            print("2. حذف فیلم")
            print("3. خروج")
            choice = input("انتخاب خود را وارد کنید: ")
            if choice == '1':
                Admin.add_movie()
            elif choice == '2':
                Admin.delete_movie()
            elif choice == '3':
                break
            else:
                print("انتخاب نامعتبر")

    @staticmethod
    def select_salone_and_movie(user_id):
        User.clear_screen()
        cinemas = Menu.execute_query_select_cinemas()
        print("\nسینماهای موجود:")
        for cinema in cinemas:
            print(f"{cinema[0]}. {cinema[1]} - {cinema[2]}")
        cinema_id = input("شناسه سینما را وارد کنید: ")
        salones = Menu.execute_query_select_salones(cinema_id)
        print("\nسالن‌های موجود:")
        for salone in salones:
            print(f"{salone[0]}. {salone[1]} - تعداد کل صندلی‌ها: {salone[2]}")
        salone_id = input("شناسه سالن را وارد کنید: ")
        movies = Menu.execute_query_select_movies(cinema_id)
        print("\nفیلم‌های موجود:")
        for movie in movies:
            print(f"{movie[0]}. {movie[1]} - {movie[2]} (تاریخ اکران: {movie[3]})")
        movie_id = input("شناسه فیلم را وارد کنید: ")
        print("سالن و فیلم با موفقیت انتخاب شدند")

    @staticmethod
    def buy_ticket(user_id):
        User.clear_screen()
        movie_id = input("شناسه فیلم را وارد کنید: ")
        seat_number = input("شماره صندلی را وارد کنید: ")
        available_seats = Menu.execute_query_check_seats(movie_id)
        if available_seats and int(seat_number) <= available_seats[0][0]:
            try:
                Menu.execute_query_buy_ticket(user_id, movie_id, seat_number)
                print("بلیط با موفقیت خریداری شد")
            except Exception as e:
                print(f"خطا: {e}")
        else:
            print("شماره صندلی نامعتبر یا هیچ صندلی موجود نیست")

    @staticmethod
    def buy_subscription(user_id):
        User.clear_screen()
        plan_name = input("نام طرح اشتراک را وارد کنید: ")
        start_date = input("تاریخ شروع را وارد کنید (YYYY-MM-DD): ")
        end_date = input("تاریخ پایان را وارد کنید (YYYY-MM-DD): ")
        try:
            Menu.execute_query_buy_subscription(user_id, plan_name, start_date, end_date)
            print("اشتراک با موفقیت خریداری شد")
        except Exception as e:
            print(f"خطا: {e}")

    @staticmethod
    def execute_query_select_cinemas():
        query = '''
        SELECT CinemaID, CinemaName, Location FROM Cinemas
        '''
        return Database.fetch(query)

    @staticmethod
    def execute_query_select_salones(cinema_id):
        query = '''
        SELECT SalonID, RowCount, ColumnCount FROM Salons WHERE CinemaID = ?
        '''
        params = (cinema_id,)
        return Database.fetch(query, params)

    @staticmethod
    def execute_query_select_movies(cinema_id):
        query = '''
        SELECT MovieID, MovieName, AgeRating, ShowTime FROM Movies WHERE CinemaID = ?
        '''
        params = (cinema_id,)
        return Database.fetch(query, params)

    @staticmethod
    def execute_query_check_seats(movie_id):
        query = '''
        SELECT AvailableSeats FROM Movies WHERE MovieID = ?
        '''
        params = (movie_id,)
        return Database.fetch(query, params)

    @staticmethod
    def execute_query_buy_ticket(user_id, movie_id, seat_number):
        query = '''
        INSERT INTO Tickets (UserID, MovieID, SeatNumber)
        VALUES (?, ?, ?)
        '''
        params = (user_id, movie_id, seat_number)
        Database.execute(query, params)

    @staticmethod
    def execute_query_buy_subscription(user_id, plan_name, start_date, end_date):
        query = '''
        INSERT INTO Subscriptions (UserID, PlanName, StartDate, EndDate)
        VALUES (?, ?, ?, ?)
        '''
        params = (user_id, plan_name, start_date, end_date)
        Database.execute(query, params)

    @staticmethod
    def main_menu():
        while True:
            User.clear_screen()
            print("\nمنوی اصلی")
            print("1. ثبت نام")
            print("2. ورود")
            print("3. خروج")
            choice = input("انتخاب خود را وارد کنید: ")
            if choice == '1':
                User.register()
            elif choice == '2':
                user_id, is_admin = User.login()
                if user_id:
                    if is_admin:
                        Menu.admin_menu()
                    else:
                        Menu.user_menu(user_id)
            elif choice == '3':
                break
            else:
                print("انتخاب نامعتبر")


if __name__ == '__main__':
    Menu.main_menu()
