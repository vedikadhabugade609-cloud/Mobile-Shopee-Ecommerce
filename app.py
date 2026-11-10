from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("admissions.db")

PROGRAMS = [
    "B.Tech Computer Science",
    "B.Tech Information Technology",
    "B.Tech Electronics and Communication",
    "BBA",
    "BCA",
    "B.Sc. Data Science",
    "MBA"
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                program TEXT NOT NULL,
                qualification TEXT NOT NULL,
                marks TEXT NOT NULL,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/")
def home():
    return render_template("index.html", programs=PROGRAMS)

@app.route("/programs")
def programs():
    return render_template("programs.html", programs=PROGRAMS)

@app.route("/apply", methods=["GET", "POST"])
def apply():
    if request.method == "POST":
        data = {
            "full_name": request.form.get("full_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "program": request.form.get("program", "").strip(),
            "qualification": request.form.get("qualification", "").strip(),
            "marks": request.form.get("marks", "").strip(),
            "message": request.form.get("message", "").strip()
        }
        if not all(data[k] for k in ["full_name", "email", "phone", "program", "qualification", "marks"]):
            flash("Please complete all required fields.", "error")
            return render_template("apply.html", programs=PROGRAMS, form=data)
        if data["program"] not in PROGRAMS:
            flash("Please choose a valid program.", "error")
            return render_template("apply.html", programs=PROGRAMS, form=data)

        with get_db() as conn:
            conn.execute("""
                INSERT INTO applications
                (full_name, email, phone, program, qualification, marks, message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, tuple(data.values()))
        return redirect(url_for("success"))
    return render_template("apply.html", programs=PROGRAMS, form={})

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/admin")
def admin():
    # Demo page only. Add authentication before using this on a public server.
    with get_db() as conn:
        applications = conn.execute(
            "SELECT * FROM applications ORDER BY created_at DESC"
        ).fetchall()
    return render_template("admin.html", applications=applications)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
