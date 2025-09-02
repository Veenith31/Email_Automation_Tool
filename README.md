**Job Portal & Email Automation System
**This is a full-stack web application for a job portal that includes separate dashboards for users and administrators. The admin dashboard features an email automation system to communicate with candidates.

Features
User Authentication: Secure registration and login for users and admins.

Job Listings: Publicly viewable job openings that users can apply to.

Admin Dashboard: A central place for administrators to manage the application.

Candidate Management: Admins can add, view, and manage a list of candidates.

Email Automation: Send customized emails to candidates using predefined templates (e.g., interview invitations, rejection letters).

Application Tracking: Admins can view a list of all job applications.

Email Logging: Track the status of all sent emails.

Tech Stack
Frontend: HTML, CSS, JavaScript

Backend: Python with Flask

Database: MySQL

Libraries:

Flask-Cors for handling Cross-Origin Resource Sharing.

mysql-connector-python for database connectivity.

bcrypt for password hashing.

PyJWT for generating authentication tokens.

Prerequisites
Before you begin, ensure you have the following installed on your system:

Python 3.x

MySQL Server

Installation & Setup
Follow these steps to get the application up and running on your local machine.

1. Clone the Repository
Bash

git clone <your-repository-url>
cd <repository-folder>
2. Set Up the Database
Log in to your MySQL server and create a new database for the project.

SQL

CREATE DATABASE job_portal;
Use the new database and create the required tables by running the following SQL script:

SQL

USE job_portal;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user'
);

CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE job_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT,
    name VARCHAR(100),
    email VARCHAR(100),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);

CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE email_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE email_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT,
    template_id INT,
    status VARCHAR(50),
    error_message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
3. Configure the Backend
Install the required Python libraries.

Bash

pip install Flask Flask-Cors mysql-connector-python bcrypt PyJWT
Open the updated_email.py file and update the following configurations:

Database Connection: On line 16, replace "your_password" with your MySQL root password.

SMTP Settings: On lines 23-24, enter your Gmail address and a Google App Password to enable email sending.

4. Create an Admin User
Run the generate_hash.py script to create a secure hash for your admin password.

Bash

python generate_hash.py
Copy the output hash.

In your MySQL database, run the following command to insert the admin user. Replace the email, password hash, and name as needed.

SQL

INSERT INTO users (name, email, password_hash, role)
VALUES ('Admin User', 'admin@example.com', 'PASTE_YOUR_GENERATED_HASH_HERE', 'admin');
Running the Application
Start the Backend Server:
Run the main Python application from your terminal.

Bash

python updated_email.py
The server will start, typically on http://127.0.0.1:5000. Keep this terminal window open.

Access the Frontend:
Open the .html files in your web browser to use the application.

Main Page: Open index.html to see the landing page.

Admin Login: Navigate to admin_login.html to access the admin dashboard.

User Login: Use user_login.html for user access to the job listings.
