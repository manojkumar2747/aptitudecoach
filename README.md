# 🎯 Aptitude Coach

Aptitude Coach is a web-based aptitude learning and practice platform designed to help students prepare for placement and competitive aptitude tests.

The platform provides topic-wise learning, interactive quizzes, company-based questions, explanations, and an admin dashboard for managing questions.

---

## 🚀 Features

### 📝 Quiz
- Select aptitude category
- Select difficulty level
- Practice multiple-choice questions
- Get instant score after completing the quiz
- View explanations for questions

### 📚 Learn Topics
- Topic-wise aptitude questions
- View questions with answers
- Detailed explanations
- Learn concepts without quiz pressure

### 🏢 Company-Based Questions
- Practice company-oriented aptitude questions
- Questions can be categorized by companies such as:
  - TCS
  - Infosys
  - Zoho
  - Google
  - Other companies

### 🔐 Admin Dashboard
- Admin login
- Add aptitude questions
- Select category, topic and difficulty
- Assign questions to companies
- Control whether questions appear in:
  - Quiz
  - Learn Topics
- Delete questions

### 🤖 AI Question Generation
Aptitude Coach uses Google's Gemini API to generate aptitude questions automatically.

Generated questions include:

- Question
- Four options
- Correct answer
- Explanation
- Category
- Topic
- Difficulty
- Company

### 💾 Database
Questions are stored using SQLite.

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Database
- SQLite

### AI
- Google Gemini API

### Deployment
- GitHub
- Render

---

## 📂 Project Structure

```text
aptitude-coach/
│
├── app.py
├── populate_db.py
├── test_gemini.py
├── aptitude.db
├── requirements.txt
├── .gitignore
│
├── static/
│   └── style.css
│
└── templates/
    ├── index.html
    ├── quiz.html
    ├── quiz_setup.html
    ├── learn.html
    ├── learn_questions.html
    ├── company_questions.html
    ├── admin.html
    └── admin_login.html
