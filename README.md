# Online Quiz Application

A beginner-friendly multiple-choice quiz built with Python, Flask, HTML, CSS, JavaScript, and SQLite.

## Features

- Ten multiple-choice questions with four options each
- Five-minute countdown that submits the quiz when time runs out
- Server-side score calculation
- Leaderboard ranked by score and then completion time
- SQLite result history (up to 50 recent attempts)
- Responsive layout for desktop and mobile

## Run on Windows

Open this folder in VS Code, then run these commands in the terminal:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Keep the terminal open while using the app.

The SQLite database is created automatically at `instance/quiz.db`.

## Project structure

```text
online_quiz_application/
├── app.py
├── requirements.txt
├── README.md
├── instance/                 # Created automatically; contains quiz.db
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── history.html
    ├── index.html
    ├── leaderboard.html
    ├── quiz.html
    └── result.html
```

## How to use

1. Enter a participant name and start the quiz.
2. Select an answer for each question before the timer reaches zero.
3. Review the score and answer feedback on the results page.
4. Open **Leaderboard** to compare scores or **History** to see recent attempts.
