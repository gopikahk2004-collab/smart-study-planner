# 📚 Smart Study Planner — StudyFlow

A Flask + SQLite study planner that creates a personalized study schedule from subjects, chapters, exam dates, difficulty and daily study hours.

## Features

- Add and delete subjects
- Exam-date tracking
- Difficulty-based planning
- Automatic study-plan generation
- Daily task completion tracking
- Overall progress percentage
- 25-minute Pomodoro timer
- Dark/light mode
- Responsive design
- SQLite database
- JSON endpoint for today's tasks

## 1. Open the project

Extract the ZIP and open the `smart-study-planner` folder in VS Code.

## 2. Create virtual environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install Flask

```bash
pip install -r requirements.txt
```

## 4. Run

```bash
python3 app.py
```

Then open:

http://127.0.0.1:5000

## 5. GitHub

```bash
git init
git add .
git commit -m "Create Smart Study Planner"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Suggested GitHub description

> A responsive Flask-based Smart Study Planner that generates personalized study schedules based on exam dates, subject difficulty, chapters and available study time.

## Future upgrades

- User login/signup
- AI-powered study recommendations
- Calendar view
- Charts with study analytics
- Email reminders
- Multiple exam support
- PostgreSQL deployment
