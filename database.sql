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
