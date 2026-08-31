from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import date, datetime, timedelta
from utils.planner import generate_plan

app = Flask(__name__)
DB = "study.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            chapters TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            hours_per_day REAL NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            chapter TEXT NOT NULL,
            task_date TEXT NOT NULL,
            minutes INTEGER NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    subjects = conn.execute("SELECT * FROM subjects ORDER BY exam_date").fetchall()
    total = conn.execute("SELECT COUNT(*) AS n FROM tasks").fetchone()["n"]
    done = conn.execute("SELECT COUNT(*) AS n FROM tasks WHERE completed=1").fetchone()["n"]
    conn.close()
    progress = round(done / total * 100) if total else 0
    return render_template("index.html", subjects=subjects, progress=progress, total=total, done=done)

@app.route("/subjects", methods=["GET", "POST"])
def subjects():
    if request.method == "POST":
        name = request.form["name"].strip()
        chapters = request.form["chapters"].strip()
        difficulty = request.form["difficulty"]
        exam_date = request.form["exam_date"]
        hours = float(request.form["hours_per_day"])

        conn = get_db()
        conn.execute(
            "INSERT INTO subjects (name, chapters, difficulty, exam_date, hours_per_day) VALUES (?, ?, ?, ?, ?)",
            (name, chapters, difficulty, exam_date, hours)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("subjects"))

    conn = get_db()
    rows = conn.execute("SELECT * FROM subjects ORDER BY exam_date").fetchall()
    conn.close()
    return render_template("subjects.html", subjects=rows)

@app.post("/subjects/delete/<int:subject_id>")
def delete_subject(subject_id):
    conn = get_db()
    conn.execute("DELETE FROM subjects WHERE id=?", (subject_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("subjects"))

@app.route("/planner", methods=["GET", "POST"])
def planner():
    conn = get_db()
    if request.method == "POST":
        conn.execute("DELETE FROM tasks")
        subjects = conn.execute("SELECT * FROM subjects").fetchall()
        plan = generate_plan(subjects)
        for item in plan:
            conn.execute(
                "INSERT INTO tasks (subject, chapter, task_date, minutes) VALUES (?, ?, ?, ?)",
                (item["subject"], item["chapter"], item["date"], item["minutes"])
            )
        conn.commit()

    tasks = conn.execute("SELECT * FROM tasks ORDER BY task_date, id").fetchall()
    conn.close()
    return render_template("planner.html", tasks=tasks)

@app.post("/task/<int:task_id>/toggle")
def toggle_task(task_id):
    conn = get_db()
    conn.execute("""
        UPDATE tasks
        SET completed = CASE WHEN completed=1 THEN 0 ELSE 1 END
        WHERE id=?
    """, (task_id,))
    conn.commit()
    conn.close()
    return redirect(request.referrer or url_for("planner"))

@app.get("/api/today")
def today():
    today_str = date.today().isoformat()
    conn = get_db()
    tasks = conn.execute(
        "SELECT * FROM tasks WHERE task_date=? ORDER BY id", (today_str,)
    ).fetchall()
    conn.close()
    return jsonify([dict(t) for t in tasks])

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
