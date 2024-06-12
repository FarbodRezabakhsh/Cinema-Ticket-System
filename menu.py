import hashlib
import getpass
import os

# External functions for executing database queries
# from external_database_module import execute_query_register, execute_query_login, execute_query_add_movie, execute_query_delete_movie, execute_query_select_salone_and_movie, execute_query_buy_ticket, execute_query_buy_subscription

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Clear the terminal screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Register new user
def register():
    clear_screen()
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    birth_date = input("Enter birth date (YYYY-MM-DD): ")

    try:
        execute_query_register(username, hash_password(password), email, phone, birth_date)
        print("Registration successful")
    except Exception as e:
        print(f"Error: {e}")

# Login user
def login():
    clear_screen()
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    user = execute_query_login(username, hash_password(password))
    if user:
        print("Login successful")
        return user[0], user[1]
    else:
        print("Invalid credentials")
        return None, None

# Add movie (Admin)
def add_movie():
    clear_screen()
    title = input("Enter movie title: ")
    description = input("Enter movie description: ")
    release_date = input("Enter release date (YYYY-MM-DD): ")
    cinema_id = input("Enter cinema ID: ")

    execute_query_add_movie(title, description, release_date, cinema_id)
    print("Movie added successfully")

# Delete movie (Admin)
def delete_movie():
    clear_screen()
    movie_id = input("Enter movie ID to delete: ")

    execute_query_delete_movie(movie_id)
    print("Movie deleted successfully")

# User menu
def user_menu(user_id):
    while True:
        clear_screen()
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
        clear_screen()
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
    clear_screen()
    cinemas = execute_query_select_salone_and_movie()

    print("\nAvailable Cinemas:")
    for cinema in cinemas:
        print(f"{cinema[0]}. {cinema[1]} - {cinema[2]}")

    cinema_id = input("Enter cinema ID: ")
    salones = execute_query_select_salone_and_movie(cinema_id)

    print("\nAvailable Salones:")
    for salone in salones:
        print(f"{salone[0]}. {salone[1]} - Total seats: {salone[2]}")

    salone_id = input("Enter salone ID: ")
    movies = execute_query_select_salone_and_movie(cinema_id)

    print("\nAvailable Movies:")
    for movie in movies:
        print(f"{movie[0]}. {movie[1]} - {movie[2]} (Release date: {movie[3]})")

    movie_id = input("Enter movie ID: ")

    print("Selected salone and movie successfully")

# Buy ticket
def buy_ticket(user_id):
    clear_screen()
    movie_id = input("Enter movie ID: ")
    seat_number = input("Enter seat number: ")

    available_seats = execute_query_buy_ticket(movie_id)

    if available_seats and int(seat_number) <= available_seats[0][0]:
        execute_query_buy_ticket(user_id, movie_id, seat_number)
        execute_query_buy_ticket(movie_id)
        print("Ticket purchased successfully")
    else:
        print("Invalid seat number or no available seats")

# Buy subscription
def buy_subscription(user_id):
    clear_screen()
    plan_name = input("Enter subscription plan name: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    execute_query_buy_subscription(user_id, plan_name, start_date, end_date)
    print("Subscription purchased successfully")

# Main menu
def main_menu():
    while True:
        clear_screen()
        print("\nMain Menu")
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register()
        elif choice == '2':
            user_id, is_admin = login()
            if user_id:
                if is_admin:
                    admin_menu()
                else:
                    user_menu(user_id)
        elif choice == '3':
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    while True:
        main_menu()
