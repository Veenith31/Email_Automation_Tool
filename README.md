Job Portal & Email Automation System

A full-stack web application that streamlines the recruitment process with separate dashboards for users and administrators.
The Admin Dashboard includes a powerful email automation system to communicate with candidates using predefined templates.

✨ Features
👤 User Features

🔐 Authentication – Secure user & admin login/registration

📋 Job Listings – Browse all available jobs

📝 Apply for Jobs – Submit applications easily

📊 Application Tracking – Track your job applications

👨‍💼 Admin Features

🖥 Admin Dashboard – Manage jobs, users, and candidates

👥 Candidate Management – Add, edit, and remove candidate records

💼 Job Management – Post, update, or remove job listings

📧 Email Automation – Send interview invites, rejection letters, or custom emails using templates

🗂 Email Logging – Track sent emails and errors

🛠 Tech Stack

Frontend:

HTML, CSS, JavaScript

Backend:

Python (Flask)

Database:

MySQL

Libraries & Tools:

Flask – Web framework

Flask-Cors – Handle CORS

mysql-connector-python – Database connectivity

bcrypt – Secure password hashing

PyJWT – Authentication with JSON Web Tokens

⚙️ Prerequisites

Make sure you have installed:

Python 3.x

MySQL Server

Git

🚀 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/job-portal-email-automation.git
cd job-portal-email-automation

2️⃣ Set Up the Database

Login to MySQL and create the database:

CREATE DATABASE job_portal;
USE job_portal;


Create the required tables:

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

3️⃣ Configure the Backend

Install dependencies:

pip install Flask Flask-Cors mysql-connector-python bcrypt PyJWT


Edit updated_email.py:

Replace your_password (line 16) with your MySQL root password

Enter your Gmail & App Password (lines 23–24) for SMTP email sending

4️⃣ Create an Admin User

Generate a secure password hash:

python generate_hash.py


Copy the generated hash and insert an admin record into MySQL:

INSERT INTO users (name, email, password_hash, role) 
VALUES ('Admin User', 'admin@example.com', 'PASTE_YOUR_GENERATED_HASH_HERE', 'admin');

5️⃣ Run the Application

Start the backend server:

python updated_email.py


Server will run on: http://127.0.0.1:5000

Open frontend files in your browser:

Main Page: index.html

Admin Login: admin_login.html

User Login: user_login.html
