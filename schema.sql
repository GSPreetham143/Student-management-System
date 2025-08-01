-- MySQL schema for Student Management System

CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    role ENUM('student', 'admin') NOT NULL
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exam Results table
CREATE TABLE IF NOT EXISTS exam_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    marks INT NOT NULL,
    grade VARCHAR(2),
    exam_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS timetable (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Dummy data

-- Passwords are pre-hashed for demo: 'admin123' and 'student123' using werkzeug.security.generate_password_hash
INSERT INTO users (username, password_hash, role) VALUES
('admin', 'admin123', 'admin'),
('student', 'student123', 'student');

INSERT INTO notifications (message) VALUES
('Welcome to the Student Management Portal!'),
('Exam results will be published next week.'),
('Timetable updated for the new semester.');

INSERT INTO exam_results (user_id, subject, marks, grade, exam_date) VALUES
(2, 'Mathematics', 85, 'A', '2025-03-15'),
(2, 'Science', 78, 'B', '2025-03-16'),
(2, 'English', 92, 'A+', '2025-03-17');

INSERT INTO timetable (user_id, day_of_week, subject, start_time, end_time) VALUES
(2, 'Monday', 'Mathematics', '09:00:00', '10:00:00'),
(2, 'Monday', 'Science', '10:15:00', '11:15:00'),
(2, 'Tuesday', 'English', '09:00:00', '10:00:00');
