# ادغام کلاس ادمین در منو انجام شده و نیازی به فایل دیگری برای ان نیست 
import hashlib
import getpass
import os
from datetime import datetime
from comment_finall import Comment
from mysql_conncetor import * 
# تنها کد های ticket  باید ایمپورت شود
class User:
    @staticmethod
    def hash_password(password):
        """این متد رمز عبور را با استفاده از الگوریتم SHA-256 هش می‌کند."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def clear_screen():
        """این متد صفحه کنسول را پاک می‌کند."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def register():
        """این متد برای ثبت نام کاربر جدید استفاده می‌شود."""
        User.clear_screen()
        username = input("نام کاربری را وارد کنید: ")
        password = getpass.getpass("رمز عبور را وارد کنید: ")
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
        """این متد برای ورود کاربر استفاده می‌شود."""
        User.clear_screen()
        username = input("نام کاربری را وارد کنید: ")
        password = getpass.getpass("رمز عبور را وارد کنید: ")
        user = User.execute_query_login(username, User.hash_password(password))
        if user:
            print("ورود با موفقیت انجام شد")
            return user[0], user[1]
        else:
            print("اعتبارنامه نادرست")
            return None, None

    @staticmethod
    def execute_query_register(username, password, email, phone, birth_date):
        """این متد کوئری SQL برای ثبت نام کاربر جدید را اجرا می‌کند."""
        query = '''
        INSERT INTO Users (username, password, email, phone, birth_date)
        VALUES (%s, %s, %s, %s, %s)
        '''
        val = (username, password, email, phone, birth_date)
        Exe(query, val)

    @staticmethod
    def execute_query_login(username, password):
        """این متد کوئری SQL برای ورود کاربر را اجرا می‌کند."""
        query = '''
        SELECT user_id, is_admin FROM Users
        WHERE username = %s AND password = %s
        '''
        val = (username, password)
        result = Get(query, val)
        return result

class Admin:
    @staticmethod
    def add_movie():
        """این متد برای اضافه کردن فیلم جدید توسط مدیر استفاده می‌شود."""
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
        """این متد برای حذف فیلم توسط مدیر استفاده می‌شود."""
        User.clear_screen()
        movie_id = input("شناسه فیلم برای حذف را وارد کنید: ")
        try:
            Admin.execute_query_delete_movie(movie_id)
            print("فیلم با موفقیت حذف شد")
        except Exception as e:
            print(f"خطا: {e}")

    @staticmethod
    def execute_query_add_movie(title, description, release_date, cinema_id):
        """این متد کوئری SQL برای اضافه کردن فیلم جدید را اجرا می‌کند."""
        query = '''
        INSERT INTO Movies (title, description, release_date, cinema_id)
        VALUES (%s, %s, %s, %s)
        '''
        val = (title, description, release_date, cinema_id)
        Exe(query, val)

    @staticmethod
    def execute_query_delete_movie(movie_id):
        """این متد کوئری SQL برای حذف فیلم را اجرا می‌کند."""
        query = '''
        DELETE FROM Movies
        WHERE movie_id = %s
        '''
        val = (movie_id, )
        Exe(query, val)

class Menu:
    @staticmethod
    def add_comment(user_id):
        """این متد برای اضافه کردن نظر توسط کاربر استفاده می‌شود."""
        User.clear_screen()
        comment_text = input("نظر خود را وارد کنید: ")
        comment_id = int(input("شناسه نظر را وارد کنید: "))
        release_date = datetime.now()
        reply = input("پاسخ (در صورت وجود) را وارد کنید: ")
        comment = Comment(comment_text, user_id, comment_id, release_date, reply)
        try:
            comment.define_comment()
            print("نظر با موفقیت اضافه شد")
        except Exception as e:
            print(f"خطا: {e}")

    @staticmethod
    def delete_comment():
        """این متد برای حذف نظر استفاده می‌شود."""
        User.clear_screen()
        comment_id = int(input("شناسه نظر برای حذف را وارد کنید: "))
        try:
            Comment.delete_comment(comment_id)
            print("نظر با موفقیت حذف شد")
        except Exception as e:
            print(f"خطا: {e}")

    @staticmethod
    def user_menu(user_id):
        """این متد منوی کاربر را نمایش می‌دهد."""
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
        """این متد منوی مدیر را نمایش می‌دهد."""
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
        """این متد برای انتخاب سالن و فیلم توسط کاربر استفاده می‌شود."""
        User.clear_screen()
        cinemas = Menu.execute_query_select_salone_and_movie()
        print("\nسینماهای موجود:")
        for cinema in cinemas:
            print(f"{cinema[0]}. {cinema[1]} - {cinema[2]}")
        cinema_id = input("شناسه سینما را وارد کنید: ")
        salones = Menu.execute_query_select_salone_and_movie(cinema_id)
        print("\nسالن‌های موجود:")
        for salone in salones:
            print(f"{salone[0]}. {salone[1]} - تعداد کل صندلی‌ها: {salone[2]}")
        salone_id = input("شناسه سالن را وارد کنید: ")
        movies = Menu.execute_query_select_salone_and_movie(cinema_id)
        print("\nفیلم‌های موجود:")
        for movie in movies:
            print(f"{movie[0]}. {movie[1]} - {movie[2]} (تاریخ اکران: {movie[3]})")
        movie_id = input("شناسه فیلم را وارد کنید: ")
        print("سالن و فیلم با موفقیت انتخاب شدند")

    @staticmethod
    def buy_ticket(user_id):
        """این متد برای خرید بلیط توسط کاربر استفاده می‌شود."""
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
        """این متد برای خرید اشتراک توسط کاربر استفاده می‌شود."""
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
    def execute_query_select_salone_and_movie(cinema_id=None):
        """این متد کوئری SQL برای انتخاب سالن و فیلم را اجرا می‌کند."""
        if cinema_id:
            query = '''
            SELECT salone_id, salone_name, total_seats
            FROM Salones
            WHERE cinema_id = %s
            '''
            val = (cinema_id, )
        else:
            query = '''
            SELECT cinema_id, cinema_name, location
            FROM Cinemas
            '''
            val = ()
        return Get(query, val)

    @staticmethod
    def execute_query_check_seats(movie_id):
        """این متد کوئری SQL برای بررسی تعداد صندلی‌های موجود را اجرا می‌کند."""
        query = '''
        SELECT available_seats
        FROM Movies
        WHERE movie_id = %s
        '''
        val = (movie_id, )
        return Get(query, val)

    @staticmethod
    def execute_query_buy_ticket(user_id, movie_id, seat_number):
        """این متد کوئری SQL برای خرید بلیط توسط کاربر را اجرا می‌کند."""
        query = '''
        INSERT INTO Tickets (user_id, movie_id, seat_number)
        VALUES (%s, %s, %s)
        '''
        val = (user_id, movie_id, seat_number)
        Exe(query, val)

    @staticmethod
    def execute_query_buy_subscription(user_id, plan_name, start_date, end_date):
        """این متد کوئری SQL برای خرید اشتراک را اجرا می‌کند."""
        query = '''
        INSERT INTO Subscriptions (user_id, plan_name, start_date, end_date)
        VALUES (%s, %s, %s, %s)
        '''
        val = (user_id, plan_name, start_date, end_date)
        Exe(query, val)

    @staticmethod
    def main_menu():
        """این متد منوی اصلی را نمایش می‌دهد."""
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
