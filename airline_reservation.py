import mysql.connector

# -----------------------------
# Database Connection
# -----------------------------
def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="password",  # Replace with your MySQL password
        database="airline_reservation"
    )

# -----------------------------
# Database Initialization
# -----------------------------
def setup_database():
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INT AUTO_INCREMENT PRIMARY KEY,
            origin VARCHAR(100),
            destination VARCHAR(100),
            date DATE,
            seats_available INT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE,
            password VARCHAR(100)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            flight_id INT,
            status VARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# User Registration
# -----------------------------
def register_user():
    conn = connect_database()
    cursor = conn.cursor()

    print("\n--- User Registration ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                       (username, password))
        conn.commit()
        print("Registration successful!")
    except mysql.connector.IntegrityError:
        print("Username already exists. Try again.")

    conn.close()


# -----------------------------
# User Login
# -----------------------------
def login_user():
    conn = connect_database()
    cursor = conn.cursor()

    print("\n--- User Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT user_id FROM users WHERE username=%s AND password=%s",
                   (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print("Login successful!")
        return user[0]
    else:
        print("Invalid credentials.")
        return None


# -----------------------------
# Admin Flight Management
# -----------------------------
def manage_flights():
    conn = connect_database()
    cursor = conn.cursor()

    print("\n--- Admin Flight Management ---")
    print("1. Add Flight")
    print("2. View Flights")
    print("3. Delete Flight")

    choice = int(input("Enter choice: "))

    if choice == 1:
        origin = input("Enter origin: ")
        destination = input("Enter destination: ")
        date = input("Enter date (YYYY-MM-DD): ")
        seats = int(input("Enter available seats: "))

        cursor.execute("""
            INSERT INTO flights (origin, destination, date, seats_available)
            VALUES (%s, %s, %s, %s)
        """, (origin, destination, date, seats))

        conn.commit()
        print("Flight added successfully!")

    elif choice == 2:
        cursor.execute("SELECT * FROM flights")
        flights = cursor.fetchall()

        print("\n--- Available Flights ---")
        for f in flights:
            print(f"ID: {f[0]}, Origin: {f[1]}, Destination: {f[2]}, Date: {f[3]}, Seats: {f[4]}")

    elif choice == 3:
        flight_id = int(input("Enter Flight ID to delete: "))
        cursor.execute("DELETE FROM flights WHERE flight_id=%s", (flight_id,))
        conn.commit()
        print("Flight deleted successfully!")

    conn.close()


# -----------------------------
# Search Flights
# -----------------------------
def search_flights():
    conn = connect_database()
    cursor = conn.cursor()

    print("\n--- Search Flights ---")
    origin = input("Origin: ")
    destination = input("Destination: ")
    date = input("Date (YYYY-MM-DD): ")

    cursor.execute("""
        SELECT * FROM flights 
        WHERE origin=%s AND destination=%s AND date=%s
    """, (origin, destination, date))

    flights = cursor.fetchall()
    conn.close()

    if flights:
        print("\n--- Matching Flights ---")
        for f in flights:
            print(f"ID: {f[0]}, Origin: {f[1]}, Destination: {f[2]}, Date: {f[3]}, Seats: {f[4]}")
    else:
        print("No flights found.")


# -----------------------------
# Book Ticket
# -----------------------------
def book_ticket(user_id):
    conn = connect_database()
    cursor = conn.cursor()

    print("\n--- Book Ticket ---")
    flight_id = int(input("Enter Flight ID: "))

    cursor.execute("SELECT seats_available FROM flights WHERE flight_id=%s", 
                   (flight_id,))
    flight = cursor.fetchone()

    if flight and flight[0] > 0:
        cursor.execute("""
            INSERT INTO bookings (user_id, flight_id, status)
            VALUES (%s, %s, 'Booked')
        """, (user_id, flight_id))

        cursor.execute("""
            UPDATE flights SET seats_available = seats_available - 1
            WHERE flight_id=%s
        """, (flight_id,))

        conn.commit()
        print("Ticket booked successfully!")
    else:
        print("Flight unavailable.")

    conn.close()


# -----------------------------
# View Bookings
# -----------------------------
def view_bookings(user_id):
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.booking_id, f.origin, f.destination, f.date, b.status
        FROM bookings b
        JOIN flights f ON b.flight_id = f.flight_id
        WHERE b.user_id=%s
    """, (user_id,))

    bookings = cursor.fetchall()
    conn.close()

    print("\n--- Your Bookings ---")
    if bookings:
        for b in bookings:
            print(f"Booking ID: {b[0]}, Origin: {b[1]}, Destination: {b[2]}, Date: {b[3]}, Status: {b[4]}")
    else:
        print("No bookings found.")


# -----------------------------
# Main Program
# -----------------------------
def main():
    setup_database()

    print("\n=== Airline Reservation System ===")

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Admin (Manage Flights)")
        print("4. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            register_user()

        elif choice == 2:
            user_id = login_user()
            if user_id:
                while True:
                    print("\n--- User Menu ---")
                    print("1. Search Flights")
                    print("2. Book Ticket")
                    print("3. View Bookings")
                    print("4. Logout")

                    uc = int(input("Enter choice: "))

                    if uc == 1:
                        search_flights()
                    elif uc == 2:
                        book_ticket(user_id)
                    elif uc == 3:
                        view_bookings(user_id)
                    elif uc == 4:
                        break

        elif choice == 3:
            manage_flights()

        elif choice == 4:
            print("Thanks for using the system!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()