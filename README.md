# ✈️ Airline Reservation System

A simple Python + MySQL based Airline Reservation System that allows users to register, log in, search flights, book tickets, and view their bookings.  
This project was created as a Class 12 Computer Science project.

---

## 📌 Features
- User Registration & Login  
- Search Flights  
- Book Tickets  
- View Booking History  
- Admin Panel to Add/Delete Flights  
- MySQL Database Integration  

---

## 🛠️ Tech Stack
- **Python**
- **MySQL**
- **mysql-connector-python**

---

## 📂 Project Structure
airline-reservation-system/
│
├── airline_reservation.py # Main Python program
├── database.sql # Database and tables creation script
├── requirements.txt # Python dependencies
├── .gitignore # Ignored files
└── README.md # Project documentation

---

## 🚀 How to Run the Project

### 1. Install Dependencies
```bash
pip install mysql-connector-python
2. Import Database
Run this SQL script in MySQL:

sql
Copy code
CREATE DATABASE airline_reservation;
USE airline_reservation;

CREATE TABLE flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    origin VARCHAR(100),
    destination VARCHAR(100),
    date DATE,
    seats_available INT
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    flight_id INT,
    status VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
);
3. Run the Python File
bash
Copy code
python airline_reservation.py
👤 Author
Harsh Gaddhyan
Class 12 CBSE — Computer Science Project

📜 License
This project is free to use for educational purposes.

---

✔ This version will look **professional**  
✔ Correct formatting  
✔ Code blocks will render properly  
✔ Headings and emojis will appear cleanly  


Paste this into your `README.md`. If you want, I can also write your **Devfolio About Me**.
