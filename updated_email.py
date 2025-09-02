from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import ssl
from email.message import EmailMessage
import mysql.connector
import bcrypt
import jwt
import datetime

app = Flask(__name__)
CORS(app)

# MySQL Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Veeniths31@",  # <-- Change if needed
        database="job_portal"
    )

# SMTP Configuration
SMTP_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 465,
    "smtp_user": "thesummarizer31@gmail.com",
    "smtp_password": "aagt kuoq konk gbba"
}
EMAIL_SUBJECT = "Job Application Status - Congratulations!"

SECRET_KEY = "supersecretkey"

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name", "")
    email = data.get("email", "")
    password = data.get("password", "")
    role = data.get("role", "user")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (name, email, hashed, role)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully"})
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

'''@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "")
    password = data.get("password", "")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user["id"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token, "user": {"name": user["name"], "role": user["role"]}})'''

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "")
    password = data.get("password", "")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode()):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user["id"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "token": token,
        "role": user["role"],
        "name": user["name"]
    })


def send_email(smtp_config, sender_email, recipient_email, subject, body):
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_config["smtp_server"], smtp_config["smtp_port"], context=context) as server:
        server.login(smtp_config["smtp_user"], smtp_config["smtp_password"])
        server.send_message(msg)

# ---------------- API ROUTES ----------------

@app.route("/api/db-test")
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db = cursor.fetchone()[0]
        conn.close()
        return jsonify({"connected_to": db})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/candidates", methods=["GET"])
def get_candidates():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email FROM candidates")
    candidates = cursor.fetchall()
    conn.close()
    return jsonify(candidates)

@app.route("/api/candidates", methods=["POST"])
def add_candidate():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO candidates (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        conn.close()
        return jsonify({"message": "Candidate added successfully"})
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Candidate with this email already exists"}), 400

@app.route("/api/candidates/<email>", methods=["DELETE"])
def delete_candidate(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM candidates WHERE email = %s", (email,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Candidate deleted"})

@app.route("/api/template", methods=["GET"])
def get_template():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, content FROM email_templates ORDER BY id DESC LIMIT 1")
    template = cursor.fetchone()
    conn.close()
    return jsonify(template if template else {"content": ""})

@app.route("/api/template", methods=["POST"])
def update_template():
    data = request.get_json()
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "Template content is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO email_templates (title, content) VALUES (%s, %s)", ("Latest Template", content))
    conn.commit()
    conn.close()
    return jsonify({"message": "Template saved"})

@app.route("/api/send-emails", methods=["POST"])
def send_emails():
    data = request.get_json()
    incoming_candidates = data.get("candidates", [])
    template = data.get("template", "").strip()

    if not incoming_candidates:
        return jsonify({"error": "No candidates to send emails to"}), 400
    if not template:
        return jsonify({"error": "Email template is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    sender_email = SMTP_CONFIG["smtp_user"]

    # Save the template in the database
    cursor.execute("INSERT INTO email_templates (title, content) VALUES (%s, %s)", ("Send Template", template))
    template_id = cursor.lastrowid

    results = []

    for c in incoming_candidates:
        try:
            # Personalize email content
            body = template.replace("{{name}}", c["name"])

            # Send the email via SMTP
            send_email(SMTP_CONFIG, sender_email, c["email"], EMAIL_SUBJECT, body)

            # Make sure previous results are cleared before executing new statements
            cursor.execute("SELECT id FROM candidates WHERE email = %s", (c["email"],))
            candidate_id_result = cursor.fetchone()
            while cursor.nextset():  # consume any unread results
                pass

            candidate_id = candidate_id_result[0] if candidate_id_result else None

            cursor.execute("""
                INSERT INTO email_logs (candidate_id, template_id, status, error_message)
                VALUES (%s, %s, 'sent', NULL)
            """, (candidate_id, template_id))

            results.append({"email": c["email"], "status": "sent"})
        except Exception as e:
            # In case of error, log failure
            try:
                # Reuse candidate_id if it was found; if not, set to None
                cursor.execute("""
                    INSERT INTO email_logs (candidate_id, template_id, status, error_message)
                    VALUES (%s, %s, 'failed', %s)
                """, (candidate_id if 'candidate_id' in locals() else None, template_id, str(e)))
            except Exception as log_err:
                # Catch errors inserting into logs but don't interrupt the loop
                print("Logging error failed:", log_err)

            results.append({"email": c["email"], "status": "failed", "error": str(e)})

    conn.commit()
    conn.close()
    return jsonify({"results": results})

# ---------- NEW: Job-related APIs ----------

@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title, description FROM jobs ORDER BY posted_date DESC")
    jobs = cursor.fetchall()
    conn.close()
    return jsonify(jobs)

@app.route("/api/email-logs", methods=["GET"])
def get_email_logs():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT candidate_id, status, error_message, sent_at 
            FROM email_logs
            ORDER BY sent_at DESC
        """)
        logs = cursor.fetchall()
        conn.close()
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/jobs", methods=["POST"])
def add_job():
    data = request.get_json()
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, description) VALUES (%s, %s)", (title, description))
    conn.commit()
    conn.close()
    return jsonify({"message": "Job added successfully"})


@app.route("/api/applications", methods=["GET"])
def get_applications():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                a.id, 
                a.name, 
                a.email, 
                j.title AS job_title,
                a.applied_at
            FROM job_applications a
            JOIN jobs j ON a.job_id = j.id
            ORDER BY a.applied_at DESC
        """)
        results = cursor.fetchall()
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/apply", methods=["POST"])
def apply_job():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    job_id = data.get("job_id")

    if not name or not email or not job_id:
        return jsonify({"error": "Name, email, and job_id are required"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Auto-create job_applications table if not present (optional)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_applications (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_id INT,
                name VARCHAR(100),
                email VARCHAR(100),
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)

        cursor.execute(
            "INSERT INTO job_applications (job_id, name, email) VALUES (%s, %s, %s)",
            (job_id, name, email)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Application submitted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
