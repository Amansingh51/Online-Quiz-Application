# ONLINE QUIZ APPLICATION
## College Mini-Project Report

**Submitted in partial fulfillment of the requirements for:**<br>
`[Course / Degree Name]`

**Submitted by:**<br>
`[Student Name]`<br>
`[Roll Number / Registration Number]`

**Under the guidance of:**<br>
`[Project Guide Name]`

**Department:** `[Department Name]`<br>
**Institution:** `[College / University Name]`<br>
**Academic year:** `[Academic Year]`

> Replace the bracketed fields with your details before submission. This report describes the project implementation in this repository.

---

## Certificate

This is to certify that the mini-project entitled **“Online Quiz Application”** is a work carried out by **[Student Name]**, bearing **[Roll Number / Registration Number]**, under my guidance, in partial fulfillment of the requirements for **[Course / Degree Name]** during the academic year **[Academic Year]**.

| Project Guide | Head of Department | External Examiner |
|---|---|---|
| Name/signature: __________ | Name/signature: __________ | Name/signature: __________ |
| Date: __________ | Date: __________ | Date: __________ |

## Declaration

I declare that this project report entitled **“Online Quiz Application”** describes work completed for academic learning. The application uses Python, Flask, HTML, CSS, JavaScript, and SQLite. Sources and tools consulted are acknowledged in the references.

**Student name:** `[Student Name]`<br>
**Signature:** ____________________<br>
**Date:** ____________________

## Acknowledgment

I would like to thank **[Project Guide Name]**, the faculty members of **[Department Name]**, and **[College / University Name]** for their guidance and support. I also acknowledge the documentation and open-source communities behind Python, Flask, SQLite, HTML, CSS, and JavaScript.

## Abstract

The Online Quiz Application is a small web application for conducting a timed, multiple-choice quiz. A participant enters a name, answers ten questions with four options each, and receives a score with answer-by-answer feedback. A five-minute countdown runs in the browser and submits the form when it reaches zero. Quiz attempts are stored in a local SQLite database. The application also provides a leaderboard, ordered by score and then completion time, and a page showing the 50 most recent attempts.

The project uses Flask to handle web routes and HTML templates, SQLite for persistent storage, and CSS and JavaScript for the interface and timer. It is intended as a local educational demonstration and can be started on a Windows computer at `http://127.0.0.1:5000`.

**Keywords:** Online quiz, Flask, Python, SQLite, web application, multiple-choice assessment.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Requirements and Feasibility](#2-requirements-and-feasibility)
3. [System Design](#3-system-design)
4. [Implementation](#4-implementation)
5. [Testing](#5-testing)
6. [Conclusion and Future Enhancements](#6-conclusion-and-future-enhancements)
7. [References](#7-references)
8. [Appendix: Running the Project](#8-appendix-running-the-project)

---

## 1. Introduction

### 1.1 Background

Quizzes are a simple way to check knowledge and provide immediate feedback. A web-based quiz can present questions through a browser, calculate a result automatically, and keep a record of attempts without requiring paper-based marking.

### 1.2 Problem Statement

Manually preparing, checking, and recording short quizzes takes time. The project addresses this by providing a small local web application that presents fixed multiple-choice questions, calculates a participant's score, and stores the result for later review.

### 1.3 Objectives

- Build a browser-based multiple-choice quiz using Flask.
- Accept and validate a participant name.
- Present ten questions with four choices each.
- Display a five-minute countdown and submit the quiz when it reaches zero.
- Calculate and display the score and answer feedback.
- Persist quiz attempts in SQLite.
- Display ranked scores and recent result history.

### 1.4 Scope

The current version is a single quiz with a fixed question bank. It is designed to run locally for demonstration and learning. It does not provide user accounts, administrator tools, online hosting, question editing, or a server-enforced deadline.

## 2. Requirements and Feasibility

### 2.1 Functional Requirements

1. The home page provides a form to start the quiz.
2. The application trims and validates the participant name (1–40 characters).
3. The quiz page displays the question bank and a countdown.
4. The submission route compares submitted choices with the server-side answer key.
5. Each completed attempt is stored with its score, duration, answers, and UTC timestamp.
6. The result page shows the score and correct answers.
7. The leaderboard displays up to 20 attempts, ordered by score descending and completion time ascending.
8. The history page displays up to 50 recent attempts.

### 2.2 Non-Functional Requirements

- The interface should be usable on desktop and mobile browsers.
- The project should be straightforward to install and run on Windows.
- The database should be created automatically on startup.
- The application should provide understandable navigation and result feedback.

### 2.3 Hardware and Software Requirements

| Category | Requirement |
|---|---|
| Hardware | Computer capable of running Python and a modern browser |
| Operating system | Windows instructions are provided; Python and Flask support other platforms |
| Language/runtime | Python 3 |
| Web framework | Flask 3.x |
| Database | SQLite (included with Python) |
| Front end | HTML, CSS, and browser JavaScript |
| Editor | Visual Studio Code or another text editor |

### 2.4 Feasibility

- **Technical:** The project uses Python's built-in SQLite support and the Flask web framework, keeping the application small and easy to run.
- **Operational:** Participants use a web browser and do not need a separate database server.
- **Economic:** The application uses free, open-source software and does not require paid services for local operation.

## 3. System Design

### 3.1 Architecture

The application follows a small browser–server–database design:

1. The browser requests a page or posts a form.
2. Flask validates input, manages the quiz session, and selects a template.
3. On submission, Python calculates the score using the server-side question answers.
4. SQLite stores the attempt.
5. Flask returns the result, leaderboard, or history page as HTML.

### 3.2 Main Components

| Component | Responsibility |
|---|---|
| `app.py` | Flask application factory, question bank, routes, score calculation, SQLite initialization |
| `templates/` | Jinja HTML templates for the home page, quiz, result, leaderboard, and history |
| `static/style.css` | Responsive visual styling |
| Browser JavaScript | Updates the countdown and submits the quiz form at zero |
| `instance/quiz.db` | Automatically created SQLite database containing attempts |
| `requirements.txt` | Lists Flask as the application dependency |

### 3.3 Application Routes

| Method and route | Purpose |
|---|---|
| `GET /` | Display the quiz landing page |
| `POST /start` | Validate a participant name and start a quiz session |
| `GET /quiz` | Display the questions and remaining client-side timer |
| `POST /submit` | Calculate the score, save the attempt, and redirect to its result |
| `GET /result/<attempt_id>` | Display a saved result and answer review |
| `GET /leaderboard` | Display the top 20 attempts |
| `GET /history` | Display the 50 most recent attempts |

### 3.4 Data Design

The application creates one SQLite table named `attempts`.

| Column | Type | Description |
|---|---|---|
| `id` | Integer primary key | Unique attempt identifier |
| `participant_name` | Text | Name entered by the participant |
| `score` | Integer | Number of correct answers |
| `total` | Integer | Number of questions in the attempt |
| `duration_seconds` | Integer | Recorded quiz duration, capped at the quiz limit |
| `answers_json` | Text | JSON answer review saved for the result page |
| `created_at` | Text | UTC timestamp for the attempt |

### 3.5 Quiz Workflow

1. The participant enters a name on the landing page.
2. Flask normalizes and validates the name, then stores the participant and quiz start time in the session.
3. The quiz page renders the fixed question bank and starts the browser countdown.
4. The participant submits answers, or the browser submits the form when its countdown reaches zero.
5. Flask compares submitted answers against the server-side answer key, calculates the score, and stores the attempt in SQLite.
6. The participant is redirected to the result page. The saved attempt is also available in history and leaderboard views.

## 4. Implementation

### 4.1 Technologies

- **Python:** Application logic and score calculation.
- **Flask:** URL routing, request handling, sessions, and template rendering.
- **SQLite:** Local persistence for quiz attempts.
- **HTML and Jinja:** Page structure and dynamic content.
- **CSS:** Layout, colors, responsive behavior, and form styling.
- **JavaScript:** Browser countdown and automatic form submission at zero.

### 4.2 Scoring and Persistence

The score is calculated on the server by comparing each submitted choice with the corresponding answer stored in the question bank. The result is inserted into SQLite using a parameterized SQL statement. The answer review is serialized as JSON and stored with the attempt.

### 4.3 Leaderboard and History

The leaderboard sorts attempts by highest score first. If scores tie, the shorter completion time ranks first; the earlier timestamp is used as the next tie-breaker. The history view sorts by most recent timestamp and displays up to 50 entries.

### 4.4 Timer Behavior and Limitations

The five-minute countdown is implemented in browser JavaScript. When it reaches zero, the browser submits the quiz form. The Flask submission route records a duration capped at five minutes, but it does not independently reject or force-submit late requests. Therefore, the countdown is suitable for a local mini-project demonstration, not for a high-stakes or tamper-resistant assessment.

## 5. Testing

### 5.1 Test Method

The application was checked with Flask's test client using a temporary SQLite database. The test exercised the main routes and a complete quiz submission without retaining test attempts in the project database.

### 5.2 Functional Test Cases

| Test | Expected result | Observed result |
|---|---|---|
| Open the landing page | HTTP 200 and rendered page | Passed |
| Start quiz with a valid name | Redirect to quiz | Passed |
| Open quiz during an active session | Questions and initial timer render | Passed |
| Submit all correct answers | Attempt saved and result redirect returned | Passed |
| Open saved result | Score and participant displayed | Passed |
| Open leaderboard and history | Pages render and include saved attempt | Passed |
| Request a nonexistent result ID | HTTP 404 | Passed |
| Start with a blank name | Validation message displayed | Passed |
| Compile Python source | No syntax error | Passed |

### 5.3 Test Summary

The checked end-to-end route flow passed for quiz start, question display, server-side scoring, result persistence, leaderboard, history, invalid-name feedback, and missing-result handling. This is a focused functional check, not a claim of exhaustive browser, load, or security testing.

## 6. Conclusion and Future Enhancements

### 6.1 Conclusion

The Online Quiz Application demonstrates how a small Python and Flask project can combine web forms, session-based quiz state, server-side scoring, a browser timer, HTML templates, responsive styling, and SQLite persistence. Participants can complete a quiz, review their results, and compare attempts.

### 6.2 Future Enhancements

- Add a question-management interface and support multiple quizzes or categories.
- Add user accounts and participant-specific history.
- Enforce quiz deadlines on the server and add protections against repeated submissions.
- Add CSRF protection and security configuration suitable for deployment.
- Add pagination, search, and export for result history.
- Add automated unit and browser-based tests.
- Deploy the application using a production WSGI server and managed configuration.

## 7. References

1. Python documentation — <https://docs.python.org/3/>
2. Flask documentation — <https://flask.palletsprojects.com/>
3. SQLite documentation — <https://www.sqlite.org/docs.html>
4. MDN Web Docs: HTML — <https://developer.mozilla.org/docs/Web/HTML>
5. MDN Web Docs: CSS — <https://developer.mozilla.org/docs/Web/CSS>
6. MDN Web Docs: JavaScript — <https://developer.mozilla.org/docs/Web/JavaScript>

## 8. Appendix: Running the Project

From the project directory in a Windows PowerShell terminal:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open <http://127.0.0.1:5000> in a browser. The application creates `instance/quiz.db` automatically. Keep the terminal open while using the local development server.
