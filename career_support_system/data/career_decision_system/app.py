import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from utils.report_generator import generate_career_report
from utils.resume_parser import clean_text, extract_resume_text
from utils.role_matcher import (
    CAREER_ROLES,
    build_recommendations,
    build_skill_gap_data,
    get_role_by_name,
)
from utils.skill_extractor import extract_skills


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
ALLOWED_EXTENSIONS = {"pdf", "docx"}
VALID_PROGRESS_STATUS = {"Not Started", "In Progress", "Completed"}
STATUS_POINTS = {"Not Started": 0, "In Progress": 1, "Completed": 2}

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = "career-support-secret-key-change-in-production"
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_column(cursor, table_name, column_name, column_sql):
    columns = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
    existing = {column[1] for column in columns}
    if column_name not in existing:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_sql}")


def table_has_column(table_name, column_name):
    conn = get_db_connection()
    columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    conn.close()
    return any(column[1] == column_name for column in columns)


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            uploaded_at TEXT NOT NULL,
            resume_text TEXT NOT NULL,
            extracted_skills TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    ensure_column(cur, "resumes", "source_type", "source_type TEXT NOT NULL DEFAULT 'file'")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            status TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(user_id, skill_name),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    ensure_column(cur, "progress", "role_name", "role_name TEXT NOT NULL DEFAULT ''")

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INTEGER PRIMARY KEY,
            selected_role TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS progress_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role_name TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            status TEXT NOT NULL,
            recorded_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    conn.commit()
    conn.close()


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_csv_field(raw):
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def latest_resume_by_user(user_id):
    conn = get_db_connection()
    resume = conn.execute(
        """
        SELECT * FROM resumes
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
        LIMIT 1
        """,
        (user_id,),
    ).fetchone()
    conn.close()
    return resume


def previous_resume_by_user(user_id):
    conn = get_db_connection()
    resume = conn.execute(
        """
        SELECT * FROM resumes
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
        LIMIT 1 OFFSET 1
        """,
        (user_id,),
    ).fetchone()
    conn.close()
    return resume


def get_selected_role(user_id):
    conn = get_db_connection()
    row = conn.execute(
        """
        SELECT selected_role
        FROM user_roles
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()
    conn.close()
    return row["selected_role"] if row else None


def set_selected_role(user_id, role_name):
    conn = get_db_connection()
    conn.execute(
        """
        INSERT INTO user_roles (user_id, selected_role, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET selected_role = excluded.selected_role, updated_at = excluded.updated_at
        """,
        (user_id, role_name, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def get_user_progress(user_id, role_name):
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT skill_name, status
        FROM progress
        WHERE user_id = ?
        """,
        (user_id,),
    ).fetchall()
    conn.close()
    return {row["skill_name"]: row["status"] for row in rows}


def upsert_progress(user_id, role_name, skill_name, status):
    timestamp = datetime.utcnow().isoformat()
    conn = get_db_connection()
    has_role_name = table_has_column("progress", "role_name")
    existing = conn.execute(
        """
        SELECT id
        FROM progress
        WHERE user_id = ? AND skill_name = ?
        LIMIT 1
        """,
        (user_id, skill_name),
    ).fetchone()

    if existing:
        if has_role_name:
            conn.execute(
                """
                UPDATE progress
                SET role_name = ?, status = ?, updated_at = ?
                WHERE id = ?
                """,
                (role_name, status, timestamp, existing["id"]),
            )
        else:
            conn.execute(
                """
                UPDATE progress
                SET status = ?, updated_at = ?
                WHERE id = ?
                """,
                (status, timestamp, existing["id"]),
            )
    else:
        if has_role_name:
            conn.execute(
                """
                INSERT INTO progress (user_id, skill_name, role_name, status, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, skill_name, role_name, status, timestamp),
            )
        else:
            conn.execute(
                """
                INSERT INTO progress (user_id, skill_name, status, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, skill_name, status, timestamp),
            )

    conn.execute(
        """
        INSERT INTO progress_history (user_id, role_name, skill_name, status, recorded_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, role_name, skill_name, status, timestamp),
    )
    conn.commit()
    conn.close()


def get_progress_history(user_id, role_name):
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT skill_name, status, recorded_at
        FROM progress_history
        WHERE user_id = ? AND role_name = ?
        ORDER BY recorded_at ASC
        """,
        (user_id, role_name),
    ).fetchall()
    conn.close()
    return rows


def compute_streak(history_rows):
    if not history_rows:
        return 0

    unique_days = []
    for row in history_rows:
        day = row["recorded_at"][:10]
        if day not in unique_days:
            unique_days.append(day)

    streak = 1
    for index in range(len(unique_days) - 1, 0, -1):
        current = datetime.fromisoformat(unique_days[index])
        previous = datetime.fromisoformat(unique_days[index - 1])
        if (current - previous).days == 1:
            streak += 1
        else:
            break
    return streak


def build_progress_timeline(history_rows):
    if not history_rows:
        return {
            "labels": ["Start"],
            "values": [0],
            "task_labels": ["No updates yet"],
            "points": [{"x": 1, "y": 0}],
        }

    labels = []
    values = []
    task_labels = []
    points = []
    for index, row in enumerate(history_rows[-10:], start=1):
        labels.append(datetime.fromisoformat(row["recorded_at"]).strftime("%d %b"))
        values.append(STATUS_POINTS.get(row["status"], 0))
        task_labels.append(f"{row['skill_name']} - {row['status']}")
        points.append({"x": index, "y": STATUS_POINTS.get(row["status"], 0)})
    return {"labels": labels, "values": values, "task_labels": task_labels, "points": points}


def get_role_score_from_resume(resume_row, role_name):
    if not resume_row or not role_name:
        return 0.0
    extracted_skills = parse_csv_field(resume_row["extracted_skills"])
    recommendations = build_recommendations(extracted_skills, CAREER_ROLES)
    selected_match = get_role_by_name(recommendations, role_name)
    return float(selected_match["match_score"]) if selected_match else 0.0


def get_dashboard_payload(user_id):
    resume = latest_resume_by_user(user_id)
    if not resume:
        return {
            "has_resume": False,
            "extracted_skills": [],
            "recommendations": [],
            "selected_role": None,
            "selected_match": None,
            "missing_skills": [],
            "learning_guidance": {},
            "reference_links": [],
            "practice_sites": [],
            "daily_plan": [],
            "progress_data": [],
            "progress_summary": {"not_started": 0, "in_progress": 0, "completed": 0},
            "streak_days": 0,
            "charts": {
                "role_labels": [],
                "role_scores": [],
                "before_after": [0, 0],
                "readiness_trend": [0, 0, 0],
                "progress_labels": ["Start"],
                "progress_values": [0],
                "progress_tasks": ["No updates yet"],
            },
        }

    extracted_skills = parse_csv_field(resume["extracted_skills"])
    recommendations = build_recommendations(extracted_skills, CAREER_ROLES)
    stored_selected_role = get_selected_role(user_id)
    selected_match = get_role_by_name(recommendations, stored_selected_role)
    if selected_match and stored_selected_role != selected_match["role"]:
        set_selected_role(user_id, selected_match["role"])

    gap_data = build_skill_gap_data(extracted_skills, selected_match)
    progress_map = get_user_progress(user_id, selected_match["role"]) if selected_match else {}

    progress_data = []
    not_started = 0
    in_progress = 0
    completed = 0
    for skill in gap_data["missing_skills"]:
        status = progress_map.get(skill, "Not Started")
        progress_data.append({"skill": skill, "status": status})
        if status == "Completed":
            completed += 1
        elif status == "In Progress":
            in_progress += 1
        else:
            not_started += 1

    current_score = float(selected_match["match_score"]) if selected_match else 0.0
    previous_resume = previous_resume_by_user(user_id)
    previous_score = get_role_score_from_resume(previous_resume, selected_match["role"]) if selected_match else 0.0

    history_rows = get_progress_history(user_id, selected_match["role"]) if selected_match else []
    timeline = build_progress_timeline(history_rows)

    charts = {
        "role_labels": [item["role"] for item in recommendations],
        "role_scores": [item["match_score"] for item in recommendations],
        "before_after": [previous_score, current_score],
        "readiness_trend": [previous_score, round((previous_score + current_score) / 2, 2), current_score],
        "progress_labels": timeline["labels"],
        "progress_values": timeline["values"],
        "progress_tasks": timeline["task_labels"],
        "progress_points": timeline["points"],
    }

    return {
        "has_resume": True,
        "resume_id": resume["id"],
        "resume_source_type": resume["source_type"],
        "extracted_skills": extracted_skills,
        "recommendations": recommendations,
        "selected_role": selected_match["role"] if selected_match else None,
        "selected_match": selected_match,
        "required_skills": selected_match["required_skills"] if selected_match else [],
        "missing_skills": gap_data["missing_skills"],
        "learning_guidance": gap_data["learning_guidance"],
        "reference_links": gap_data["reference_links"],
        "practice_sites": gap_data["practice_sites"],
        "daily_plan": gap_data["daily_plan"],
        "progress_data": progress_data,
        "progress_summary": {
            "not_started": not_started,
            "in_progress": in_progress,
            "completed": completed,
        },
        "streak_days": compute_streak(history_rows),
        "previous_score": previous_score,
        "current_score": current_score,
        "daily_updates": history_rows[-10:],
        "charts": charts,
    }


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("upload_resume"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        conn = get_db_connection()
        try:
            conn.execute(
                """
                INSERT INTO users (name, email, password, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (name, email, password, datetime.utcnow().isoformat()),
            )
            conn.commit()
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already exists. Please login directly.", "danger")
            return render_template("register.html")
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        conn = get_db_connection()
        user = conn.execute(
            """
            SELECT id, name, email
            FROM users
            WHERE email = ? AND password = ?
            """,
            (email, password),
        ).fetchone()
        conn.close()

        if not user:
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        flash("Login successful.", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You are logged out.", "info")
    return redirect(url_for("login"))


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_resume():
    if request.method == "POST":
        file = request.files.get("resume")
        resume_text_input = request.form.get("resume_text", "").strip()

        if (not file or not file.filename) and not resume_text_input:
            flash("Upload a resume file or paste resume text.", "danger")
            return redirect(url_for("upload_resume"))

        stored_name = "pasted_resume.txt"
        source_type = "text"

        try:
            if file and file.filename:
                if not allowed_file(file.filename):
                    flash("Unsupported format. Upload PDF or DOCX.", "danger")
                    return redirect(url_for("upload_resume"))

                filename = secure_filename(file.filename)
                timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
                stored_name = f"{session['user_id']}_{timestamp}_{filename}"
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], stored_name)
                file.save(filepath)
                resume_text = extract_resume_text(filepath)
                source_type = "file"
            else:
                resume_text = clean_text(resume_text_input)
                if not resume_text:
                    raise ValueError("No readable text found in the pasted resume.")

            extracted_skills = extract_skills(resume_text)
        except Exception as exc:
            flash(f"Failed to process resume: {exc}", "danger")
            return redirect(url_for("upload_resume"))

        conn = get_db_connection()
        conn.execute(
            """
            INSERT INTO resumes (user_id, filename, uploaded_at, resume_text, extracted_skills, source_type)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                stored_name,
                datetime.utcnow().isoformat(),
                resume_text,
                ",".join(extracted_skills),
                source_type,
            ),
        )
        conn.commit()
        conn.close()

        flash("Resume uploaded and analyzed successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("upload.html")


@app.route("/dashboard")
@login_required
def dashboard():
    payload = get_dashboard_payload(session["user_id"])
    return render_template("dashboard.html", user_name=session["user_name"], payload=payload)


@app.route("/select_role", methods=["POST"])
@login_required
def select_role():
    role_name = request.form.get("role_name", "").strip()
    if role_name not in CAREER_ROLES:
        flash("Please select a valid career role.", "danger")
        return redirect(url_for("dashboard"))

    set_selected_role(session["user_id"], role_name)
    flash(f"{role_name} selected for your learning plan.", "success")
    return redirect(url_for("dashboard"))


@app.route("/update_progress", methods=["POST"])
@login_required
def update_progress():
    skill = request.form.get("skill", "").strip()
    role_name = request.form.get("role_name", "").strip()
    status = request.form.get("status", "").strip()

    if not skill or role_name not in CAREER_ROLES or status not in VALID_PROGRESS_STATUS:
        flash("Invalid progress update.", "danger")
        return redirect(url_for("dashboard"))

    upsert_progress(session["user_id"], role_name, skill, status)
    flash(f"Progress updated for {skill}.", "success")
    return redirect(url_for("dashboard"))


@app.route("/report")
@login_required
def report():
    payload = get_dashboard_payload(session["user_id"])
    if not payload["has_resume"]:
        flash("Upload a resume first to generate report.", "warning")
        return redirect(url_for("upload_resume"))

    report_filename = f"career_report_user_{session['user_id']}.pdf"
    report_path = os.path.join(REPORT_DIR, report_filename)

    report_context = {
        "student_name": session["user_name"],
        "selected_role": payload["selected_role"],
        "extracted_skills": payload["extracted_skills"],
        "recommendations": payload["recommendations"],
        "required_skills": payload["required_skills"],
        "missing_skills": payload["missing_skills"],
        "learning_guidance": payload["learning_guidance"],
        "reference_links": payload["reference_links"],
        "practice_sites": payload["practice_sites"],
        "daily_plan": payload["daily_plan"],
        "progress_summary": payload["progress_summary"],
        "streak_days": payload["streak_days"],
        "previous_score": payload["previous_score"],
        "readiness_score": payload["current_score"],
        "daily_updates": payload["daily_updates"],
    }
    generate_career_report(report_path, report_context)

    return send_file(report_path, as_attachment=True, download_name="career_report.pdf")


@app.route("/report_page")
@login_required
def report_page():
    return render_template("report_page.html")


@app.route("/student_portal")
def student_portal():
    demo_payload = {
        "student_name": "Bindu Sri",
        "selected_role": "Data Analyst",
        "role_score": 72,
        "streak_days": 6,
        "extracted_skills": [
            "Python",
            "SQL",
            "HTML",
            "CSS",
            "Statistics",
            "Data Analysis",
        ],
        "matching_roles": [
            {
                "role": "Data Analyst",
                "score": 72,
                "matched": ["Python", "SQL", "Statistics", "Data Analysis"],
                "missing": ["Excel", "Power BI", "Data Visualization"],
            },
            {
                "role": "Web Developer",
                "score": 50,
                "matched": ["HTML", "CSS"],
                "missing": ["JavaScript", "React", "Git", "Responsive Design"],
            },
            {
                "role": "ML Engineer",
                "score": 42,
                "matched": ["Python", "Statistics"],
                "missing": ["Machine Learning", "TensorFlow", "Deep Learning"],
            },
        ],
        "required_skills": [
            "Python",
            "SQL",
            "Statistics",
            "Data Analysis",
            "Excel",
            "Power BI",
            "Data Visualization",
        ],
        "missing_skills": ["Excel", "Power BI", "Data Visualization"],
        "learning_plan": [
            {
                "day": 1,
                "title": "Excel basics and formulas",
                "time": "45 min",
                "status": "Completed",
            },
            {
                "day": 2,
                "title": "Pivot tables practice",
                "time": "50 min",
                "status": "Completed",
            },
            {
                "day": 3,
                "title": "Power BI data import",
                "time": "45 min",
                "status": "In Progress",
            },
            {
                "day": 4,
                "title": "Dashboard cards and charts",
                "time": "60 min",
                "status": "Not Started",
            },
            {
                "day": 5,
                "title": "Storytelling with data visuals",
                "time": "40 min",
                "status": "Not Started",
            },
        ],
        "references": [
            "https://www.youtube.com/watch?v=Vl0H-qTclOg",
            "https://www.youtube.com/watch?v=AGrl-H87pRU",
            "https://www.youtube.com/watch?v=aHaOIvR00So",
            "https://www.kaggle.com/learn/pandas",
            "https://www.sqlbolt.com/",
            "https://learn.microsoft.com/power-bi/",
            "https://www.tableau.com/learn/training",
            "https://www.khanacademy.org/math/statistics-probability",
            "https://pandas.pydata.org/docs/getting_started/index.html",
            "https://www.w3schools.com/sql/",
        ],
        "practice_sites": [
            "Kaggle",
            "SQLBolt",
            "LeetCode",
            "HackerRank",
            "Tableau Public",
            "Microsoft Learn",
        ],
        "daily_updates": [
            "Day 1: Completed Excel formulas task",
            "Day 2: Completed pivot tables task",
            "Day 3: Started Power BI import lesson",
            "Day 4: Reupload resume after dashboard practice",
        ],
        "chart_payload": {
            "role_labels": ["Data Analyst", "Web Developer", "ML Engineer"],
            "role_scores": [72, 50, 42],
            "score_compare": [48, 72],
            "progress_labels": ["Day 1", "Day 2", "Day 3", "Day 4"],
            "progress_points": [
                {"x": 1, "y": 1},
                {"x": 2, "y": 2},
                {"x": 3, "y": 2},
                {"x": 4, "y": 3},
            ],
        },
    }
    return render_template("student_portal.html", payload=demo_payload)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
