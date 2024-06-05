import mysql.connector
import hashlib
import getpass

DB_CONFIG = {
    'user': 'your_username',
    'password': 'your_password',
    'host': '127.0.0.1',
    'database': 'cinema',
}

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connect to database
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# Register new user
def register():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    email = input("Enter email: ")

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, hash_password(password), email))
        conn.commit()
        print("Registration successful")
    except mysql.connector.IntegrityError:
        print("Username or email already exists")
    finally:
        cursor.close()
        conn.close()

# Login user
def login():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, hash_password(password)))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        print("Login successful")
        return user[0]
    else:
        print("Invalid credentials")
        return None

# Admin add movie
def add_movie():
    title = input("Enter movie title: ")
    description = input("Enter movie description: ")
    release_date = input("Enter release date (YYYY-MM-DD): ")
    cinema_id = input("Enter cinema ID: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movies (title, description, release_date, cinema_id) VALUES (%s, %s, %s, %s)", 
                   (title, description, release_date, cinema_id))
    conn.commit()
    cursor.close()
    conn.close()

    print("Movie added successfully")

# Admin delete movie
def delete_movie():
    movie_id = input("Enter movie ID to delete: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    conn.commit()
    cursor.close()
    conn.close()

    print("Movie deleted successfully")

# User menu
def user_menu(user_id):
    while True:
        print("\nUser Menu")
        print("1. Select salone and movie")
        print("2. Buy ticket")
        print("3. Buy subscription")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            select_salone_and_movie(user_id)
        elif choice == '2':
            buy_ticket(user_id)
        elif choice == '3':
            buy_subscription(user_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice")

# Admin menu
def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. Add movie")
        print("2. Delete movie")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_movie()
        elif choice == '2':
            delete_movie()
        elif choice == '3':
            break
        else:
            print("Invalid choice")

# Select salone and movie
def select_salone_and_movie(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, location FROM cinemas")
    cinemas = cursor.fetchall()

    print("\nAvailable Cinemas:")
    for cinema in cinemas:
        print(f"{cinema[0]}. {cinema[1]} - {cinema[2]}")

    cinema_id = input("Enter cinema ID: ")
    cursor.execute("SELECT id, name, total_seats FROM salones WHERE cinema_id = %s", (cinema_id,))
    salones = cursor.fetchall()

    print("\nAvailable Salones:")
    for salone in salones:
        print(f"{salone[0]}. {salone[1]} - Total seats: {salone[2]}")

    salone_id = input("کد سالن مورد نظرتان را وارد کنید")
    cursor.execute("SELECT id, title, description, release_date FROM movies WHERE cinema_id = %s", (cinema_id,))
    movies = cursor.fetchall()

    print("\nAvailable Movies:")
    for movie in movies:
        print(f"{movie[0]}. {movie[1]} - {movie[2]} (تاریخ انتشار: {movie[3]})")

    movie_id = input(":کد فیلم مورد نظرتان را وارد کنید")

    print("!سالن و فیلم مورد نظرتان با موفقیت انتخاب شدند")
    cursor.close()
    conn.close()

# Buy ticket
def buy_ticket(user_id):
    movie_id = input("Enter movie ID: ")
    seat_number = input("Enter seat number: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT available_seats FROM salones WHERE id = (SELECT salone_id FROM movies WHERE id = %s)", (movie_id,))
    available_seats = cursor.fetchone()

    if available_seats and int(seat_number) <= available_seats[0]:
        cursor.execute("INSERT INTO reservations (user_id, movie_id, seat_number) VALUES (%s, %s, %s)", (user_id, movie_id, seat_number))
        cursor.execute("UPDATE salones SET total_seats = total_seats - 1 WHERE id = (SELECT salone_id FROM movies WHERE id = %s)", (movie_id,))
        conn.commit()
        print("Ticket purchased successfully")
    else:
        print("Invalid seat number or no available seats")

    cursor.close()
    conn.close()

# Buy subscription
def buy_subscription(user_id):
    plan_name = input("Enter subscription plan name: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subscriptions (user_id, plan_name, start_date, end_date) VALUES (%s, %s, %s, %s)", 
                   (user_id, plan_name, start_date, end_date))
    conn.commit()
    cursor.close()
    conn.close()

    print("Subscription purchased successfully")

# Main menu
def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
            if user_id:
                user_menu(user_id)
        elif choice == '3':
            admin_password = getpass.getpass("Enter admin password: ")
            if admin_password == 'admin':
                admin_menu()
            else:
                print("Invalid admin password")
        elif choice == '4':
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main_menu()