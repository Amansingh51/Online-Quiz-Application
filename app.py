import json
import os
import secrets
import sqlite3
import time
from datetime import datetime, timezone

from flask import Flask, abort, current_app, flash, g, redirect, render_template, request, session, url_for


QUIZ_DURATION_SECONDS = 300
QUESTIONS = [
    {
        "id": "python-list",
        "text": "Which symbol is used to create a list in Python?",
        "options": ["{}", "[]", "()", "<>"],
        "answer": "[]",
    },
    {
        "id": "html-heading",
        "text": "Which HTML tag represents the most important heading?",
        "options": ["<heading>", "<h6>", "<h1>", "<head>"],
        "answer": "<h1>",
    },
    {
        "id": "css-color",
        "text": "Which CSS property changes the text color?",
        "options": ["font-style", "background-color", "text-color", "color"],
        "answer": "color",
    },
    {
        "id": "flask",
        "text": "Flask is primarily a framework for which language?",
        "options": ["Java", "Python", "C++", "Ruby"],
        "answer": "Python",
    },
    {
        "id": "sqlite",
        "text": "Which kind of database is SQLite?",
        "options": ["A file-based relational database", "A spreadsheet", "A web browser", "A programming language"],
        "answer": "A file-based relational database",
    },
    {
        "id": "http-get",
        "text": "Which HTTP method is commonly used to retrieve a web page?",
        "options": ["POST", "DELETE", "GET", "PATCH"],
        "answer": "GET",
    },
    {
        "id": "js",
        "text": "Which keyword declares a block-scoped variable in JavaScript?",
        "options": ["varonly", "let", "define", "dim"],
        "answer": "let",
    },
    {
        "id": "python-function",
        "text": "Which keyword starts a function definition in Python?",
        "options": ["function", "func", "def", "lambda"],
        "answer": "def",
    },
    {
        "id": "css-flex",
        "text": "Which CSS value enables a flexbox layout?",
        "options": ["display: flex", "position: flex", "layout: flex", "flex: display"],
        "answer": "display: flex",
    },
    {
        "id": "sqlite-query",
        "text": "Which SQL command reads rows from a table?",
        "options": ["INSERT", "SELECT", "UPDATE", "CREATE"],
        "answer": "SELECT",
    },
]
QUESTION_BY_ID = {question["id"]: question for question in QUESTIONS}


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        DATABASE=os.path.join(app.instance_path, "quiz.db"),
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    init_db(app)

    @app.before_request
    def open_database():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row

    @app.teardown_appcontext
    def close_database(_error=None):
        database = g.pop("db", None)
        if database is not None:
            database.close()

    @app.get("/")
    def index():
        return render_template("index.html", question_count=len(QUESTIONS), duration=QUIZ_DURATION_SECONDS // 60)

    @app.post("/start")
    def start_quiz():
        name = " ".join(request.form.get("name", "").split())
        if not name or len(name) > 40:
            flash("Please enter a name between 1 and 40 characters.", "error")
            return redirect(url_for("index"))

        session.clear()
        session["participant_name"] = name
        session["question_ids"] = [question["id"] for question in QUESTIONS]
        session["quiz_started_at"] = time.time()
        return redirect(url_for("quiz"))

    @app.get("/quiz")
    def quiz():
        if not has_active_quiz():
            flash("Start a quiz before opening the question page.", "error")
            return redirect(url_for("index"))

        remaining = max(0, QUIZ_DURATION_SECONDS - int(time.time() - session["quiz_started_at"]))
        questions = [QUESTION_BY_ID[question_id] for question_id in session["question_ids"]]
        return render_template("quiz.html", questions=questions, remaining=remaining)

    @app.post("/submit")
    def submit_quiz():
        if not has_active_quiz():
            flash("There is no active quiz to submit.", "error")
            return redirect(url_for("index"))

        submitted_answers = request.form
        question_ids = session["question_ids"]
        details = []
        score = 0
        for question_id in question_ids:
            question = QUESTION_BY_ID[question_id]
            selected = submitted_answers.get(question_id, "")
            correct = selected == question["answer"]
            score += int(correct)
            details.append(
                {
                    "question": question["text"],
                    "selected": selected,
                    "answer": question["answer"],
                    "correct": correct,
                }
            )

        duration = min(QUIZ_DURATION_SECONDS, max(0, int(time.time() - session["quiz_started_at"])))
        cursor = get_db().execute(
            """
            INSERT INTO attempts (participant_name, score, total, duration_seconds, answers_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session["participant_name"],
                score,
                len(question_ids),
                duration,
                json.dumps(details),
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ),
        )
        get_db().commit()
        attempt_id = cursor.lastrowid
        session.clear()
        return redirect(url_for("result", attempt_id=attempt_id))

    @app.get("/result/<int:attempt_id>")
    def result(attempt_id):
        attempt = get_db().execute(
            "SELECT * FROM attempts WHERE id = ?", (attempt_id,)
        ).fetchone()
        if attempt is None:
            abort(404)
        details = json.loads(attempt["answers_json"])
        return render_template("result.html", attempt=attempt, details=details)

    @app.get("/leaderboard")
    def leaderboard():
        rows = get_db().execute(
            """
            SELECT participant_name, score, total, duration_seconds, created_at
            FROM attempts
            ORDER BY score DESC, duration_seconds ASC, created_at ASC
            LIMIT 20
            """
        ).fetchall()
        return render_template("leaderboard.html", attempts=rows)

    @app.get("/history")
    def history():
        rows = get_db().execute(
            """
            SELECT id, participant_name, score, total, duration_seconds, created_at
            FROM attempts
            ORDER BY created_at DESC, id DESC
            LIMIT 50
            """
        ).fetchall()
        return render_template("history.html", attempts=rows)

    def has_active_quiz():
        question_ids = session.get("question_ids")
        return (
            bool(session.get("participant_name"))
            and isinstance(question_ids, list)
            and all(question_id in QUESTION_BY_ID for question_id in question_ids)
            and isinstance(session.get("quiz_started_at"), (int, float))
        )

    return app


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db(app):
    os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)
    with sqlite3.connect(app.config["DATABASE"]) as database:
        database.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                participant_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                duration_seconds INTEGER NOT NULL,
                answers_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
