from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3

app = Flask(__name__)

# =========================================================
# APP SETTINGS
# =========================================================

app.secret_key = "aptitude-coach-secret-key"

DATABASE = "aptitude.db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# DATABASE INITIALIZATION + UPGRADE
# =========================================================

def init_db():

    conn = get_db()

    # -----------------------------------------------------
    # CREATE TABLE IF IT DOES NOT EXIST
    # -----------------------------------------------------

    conn.execute("""
        CREATE TABLE IF NOT EXISTS questions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            question TEXT NOT NULL,

            option_a TEXT DEFAULT '',
            option_b TEXT DEFAULT '',
            option_c TEXT DEFAULT '',
            option_d TEXT DEFAULT '',

            answer TEXT DEFAULT '',

            explanation TEXT DEFAULT '',

            category TEXT DEFAULT 'Quantitative Aptitude',

            topic TEXT DEFAULT 'General',

            difficulty TEXT DEFAULT 'Easy',

            company TEXT DEFAULT 'General',

            show_in_quiz INTEGER DEFAULT 1,

            show_in_learn INTEGER DEFAULT 1

        )
    """)

    conn.commit()


    # -----------------------------------------------------
    # CHECK EXISTING COLUMNS
    # -----------------------------------------------------

    columns = conn.execute(
        "PRAGMA table_info(questions)"
    ).fetchall()

    existing_columns = {
        column["name"]
        for column in columns
    }


    # -----------------------------------------------------
    # ADD MISSING COLUMNS
    # -----------------------------------------------------

    if "option_a" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN option_a TEXT DEFAULT ''
        """)


    if "option_b" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN option_b TEXT DEFAULT ''
        """)


    if "option_c" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN option_c TEXT DEFAULT ''
        """)


    if "option_d" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN option_d TEXT DEFAULT ''
        """)


    if "answer" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN answer TEXT DEFAULT ''
        """)


    if "explanation" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN explanation TEXT DEFAULT ''
        """)


    if "category" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN category TEXT
            DEFAULT 'Quantitative Aptitude'
        """)


    if "topic" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN topic TEXT
            DEFAULT 'General'
        """)


    if "difficulty" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN difficulty TEXT
            DEFAULT 'Easy'
        """)


    if "company" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN company TEXT
            DEFAULT 'General'
        """)


    if "show_in_quiz" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN show_in_quiz INTEGER
            DEFAULT 1
        """)


    if "show_in_learn" not in existing_columns:

        conn.execute("""
            ALTER TABLE questions
            ADD COLUMN show_in_learn INTEGER
            DEFAULT 1
        """)


    conn.commit()


    # -----------------------------------------------------
    # INSERT SAMPLE QUESTIONS ONLY IF EMPTY
    # -----------------------------------------------------

    count = conn.execute(
        "SELECT COUNT(*) FROM questions"
    ).fetchone()[0]


    if count == 0:

        sample_questions = [

            (
                "What is 25% of 200?",

                "25",
                "40",
                "50",
                "75",

                "50",

                "25% means 25/100. "
                "Therefore, 25/100 × 200 = 50.",

                "Quantitative Aptitude",

                "Percentages",

                "Easy",

                "TCS",

                1,
                1
            ),


            (
                "A number is increased by 20% and then "
                "decreased by 20%. What is the overall "
                "percentage change?",

                "No change",
                "2% decrease",
                "4% decrease",
                "4% increase",

                "4% decrease",

                "Assume the original number is 100. "
                "After increasing by 20%, it becomes 120. "
                "A 20% decrease of 120 is 24, giving 96. "
                "Therefore, the overall decrease is 4%.",

                "Quantitative Aptitude",

                "Percentages",

                "Medium",

                "Google",

                1,
                1
            ),


            (
                "A train travels 120 km in 2 hours. "
                "What is its speed?",

                "40 km/h",
                "50 km/h",
                "60 km/h",
                "80 km/h",

                "60 km/h",

                "Speed = Distance / Time. "
                "Therefore, 120 / 2 = 60 km/h.",

                "Quantitative Aptitude",

                "Time Speed Distance",

                "Easy",

                "Wipro",

                1,
                1
            ),


            (
                "What comes next: 2, 4, 8, 16, ?",

                "20",
                "24",
                "32",
                "36",

                "32",

                "Each number is multiplied by 2. "
                "Therefore, 16 × 2 = 32.",

                "Logical Reasoning",

                "Number Series",

                "Easy",

                "Accenture",

                1,
                1
            ),


            (
                "What is the square of 12?",

                "124",
                "144",
                "154",
                "164",

                "144",

                "The square of a number means multiplying "
                "it by itself. 12 × 12 = 144.",

                "Quantitative Aptitude",

                "Number System",

                "Easy",

                "Zoho",

                1,
                1
            )

        ]


        conn.executemany("""
            INSERT INTO questions
            (
                question,

                option_a,
                option_b,
                option_c,
                option_d,

                answer,

                explanation,

                category,

                topic,

                difficulty,

                company,

                show_in_quiz,

                show_in_learn
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, sample_questions)


        conn.commit()


    conn.close()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# QUIZ SETUP PAGE
# =========================================================

@app.route("/quiz")
def quiz_setup():

    return render_template(
        "quiz_setup.html"
    )


# =========================================================
# QUIZ PAGE
# =========================================================

@app.route("/quiz/start")
def quiz_start():

    return render_template(
        "quiz.html"
    )


# =========================================================
# GET QUIZ QUESTIONS
# =========================================================

@app.route("/api/questions")
def get_questions():

    category = request.args.get(
        "category",
        "All"
    )

    topic = request.args.get(
        "topic",
        "All"
    )

    difficulty = request.args.get(
        "difficulty",
        "All"
    )

    limit = request.args.get(
        "limit",
        5
    )


    try:

        limit = int(limit)

    except:

        limit = 5


    # Prevent invalid or excessive values

    if limit < 1:

        limit = 5

    if limit > 50:

        limit = 50


    conn = get_db()


    query = """
        SELECT *

        FROM questions

        WHERE show_in_quiz = 1
    """


    params = []


    # -----------------------------------------------------
    # CATEGORY FILTER
    # -----------------------------------------------------

    if category != "All":

        query += """
            AND category = ?
        """

        params.append(category)


    # -----------------------------------------------------
    # TOPIC FILTER
    # -----------------------------------------------------

    if topic != "All":

        query += """
            AND topic = ?
        """

        params.append(topic)


    # -----------------------------------------------------
    # DIFFICULTY FILTER
    # -----------------------------------------------------

    if difficulty != "All":

        query += """
            AND difficulty = ?
        """

        params.append(difficulty)


    # -----------------------------------------------------
    # RANDOM QUESTIONS
    # -----------------------------------------------------

    query += """
        ORDER BY RANDOM()
        LIMIT ?
    """

    params.append(limit)


    questions = conn.execute(
        query,
        params
    ).fetchall()


    conn.close()


    result = []


    for q in questions:

        result.append({

            "id": q["id"],

            "question": q["question"],

            "options": [

                q["option_a"],

                q["option_b"],

                q["option_c"],

                q["option_d"]

            ],

            "answer": q["answer"],

            "explanation": q["explanation"],

            "category": q["category"],

            "topic": q["topic"],

            "difficulty": q["difficulty"],

            "company": q["company"]

        })


    return jsonify(result)


# =========================================================
# QUIZ FILTERS
# =========================================================

@app.route("/api/filters")
def get_filters():

    conn = get_db()


    categories = conn.execute("""
        SELECT DISTINCT category

        FROM questions

        WHERE category IS NOT NULL
        AND category != ''

        ORDER BY category
    """).fetchall()


    topics = conn.execute("""
        SELECT DISTINCT topic

        FROM questions

        WHERE topic IS NOT NULL
        AND topic != ''

        ORDER BY topic
    """).fetchall()


    difficulties = conn.execute("""
        SELECT DISTINCT difficulty

        FROM questions

        WHERE difficulty IS NOT NULL
        AND difficulty != ''

        ORDER BY difficulty
    """).fetchall()


    conn.close()


    return jsonify({

        "categories": [
            x["category"]
            for x in categories
        ],

        "topics": [
            x["topic"]
            for x in topics
        ],

        "difficulties": [
            x["difficulty"]
            for x in difficulties
        ]

    })



# =========================================================
# GET TOPICS BASED ON CATEGORY
# =========================================================

@app.route("/api/topics")
def get_topics():

    category = request.args.get(
        "category",
        ""
    ).strip()

    if not category:
        return jsonify([])

    try:

        conn = get_db()

        topics = conn.execute("""
            SELECT DISTINCT topic
            FROM questions
            WHERE category = ?
            AND topic IS NOT NULL
            AND topic != ''
            ORDER BY topic
        """, (category,)).fetchall()

        conn.close()

        return jsonify([
            row["topic"]
            for row in topics
        ])

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================================================
# LEARN TOPICS PAGE
# =========================================================

@app.route("/learn")
def learn_topics():

    conn = get_db()


    topics = conn.execute("""
        SELECT

            topic,

            category,

            COUNT(*) AS question_count

        FROM questions

        WHERE show_in_learn = 1

        GROUP BY topic, category

        ORDER BY topic
    """).fetchall()


    conn.close()


    return render_template(

        "learn.html",

        topics=topics

    )


# =========================================================
# LEARN QUESTIONS FOR A TOPIC
# =========================================================

@app.route("/learn/<topic>")
def learn_topic(topic):

    conn = get_db()


    questions = conn.execute("""
        SELECT *

        FROM questions

        WHERE topic = ?

        AND show_in_learn = 1

        ORDER BY id
    """, (topic,)).fetchall()


    conn.close()


    return render_template(

        "learn_questions.html",

        questions=questions,

        topic=topic

    )


# =========================================================
# COMPANY QUESTIONS
# =========================================================

@app.route("/company/<company>")
def company_questions(company):

    conn = get_db()


    questions = conn.execute("""
        SELECT *

        FROM questions

        WHERE company = ?

        ORDER BY id
    """, (company,)).fetchall()


    conn.close()


    return render_template(

        "company_questions.html",

        questions=questions,

        company=company

    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    # Already logged in

    if session.get("admin"):

        return redirect("/admin")


    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()


        password = request.form.get(
            "password",
            ""
        )


        if (
            username == ADMIN_USERNAME
            and
            password == ADMIN_PASSWORD
        ):

            session["admin"] = True

            return redirect("/admin")


        return render_template(

            "admin_login.html",

            error="Invalid username or password"

        )


    return render_template(
        "admin_login.html"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin():

    if not session.get("admin"):

        return redirect(
            "/admin/login"
        )


    conn = get_db()


    questions = conn.execute("""
        SELECT *

        FROM questions

        ORDER BY id DESC
    """).fetchall()


    conn.close()


    return render_template(

        "admin.html",

        questions=questions

    )


# =========================================================
# ADD QUESTION
# =========================================================

@app.route(
    "/admin/add",
    methods=["POST"]
)
def add_question():

    if not session.get("admin"):

        return redirect(
            "/admin/login"
        )


    # -----------------------------------------------------
    # GET FORM DATA
    # -----------------------------------------------------

    question = request.form.get(
        "question",
        ""
    ).strip()


    option_a = request.form.get(
        "option_a",
        ""
    ).strip()


    option_b = request.form.get(
        "option_b",
        ""
    ).strip()


    option_c = request.form.get(
        "option_c",
        ""
    ).strip()


    option_d = request.form.get(
        "option_d",
        ""
    ).strip()


    answer = request.form.get(
        "answer",
        ""
    ).strip()


    explanation = request.form.get(
        "explanation",
        ""
    ).strip()


    category = request.form.get(
        "category",
        "Quantitative Aptitude"
    ).strip()


    topic = request.form.get(
        "topic",
        "General"
    ).strip()


    difficulty = request.form.get(
        "difficulty",
        "Easy"
    ).strip()


    company = request.form.get(
        "company",
        "General"
    ).strip()


    # -----------------------------------------------------
    # CHECKBOXES
    # -----------------------------------------------------

    show_in_quiz = (

        1

        if request.form.get(
            "show_in_quiz"
        )

        else 0

    )


    show_in_learn = (

        1

        if request.form.get(
            "show_in_learn"
        )

        else 0

    )


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not question:

        return "Question is required.", 400


    if not answer:

        return "Answer is required.", 400


    if not explanation:

        return "Explanation is required.", 400


    if not topic:

        topic = "General"


    if not category:

        category = "Quantitative Aptitude"


    if not difficulty:

        difficulty = "Easy"


    if not company:

        company = "General"


    # -----------------------------------------------------
    # INSERT
    # -----------------------------------------------------

    conn = get_db()


    conn.execute("""
        INSERT INTO questions
        (

            question,

            option_a,
            option_b,
            option_c,
            option_d,

            answer,

            explanation,

            category,

            topic,

            difficulty,

            company,

            show_in_quiz,

            show_in_learn

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        question,

        option_a,
        option_b,
        option_c,
        option_d,

        answer,

        explanation,

        category,

        topic,

        difficulty,

        company,

        show_in_quiz,

        show_in_learn

    ))


    conn.commit()

    conn.close()


    return redirect("/admin")


# =========================================================
# DELETE QUESTION
# =========================================================

@app.route(
    "/admin/delete/<int:question_id>"
)
def delete_question(question_id):

    if not session.get("admin"):

        return redirect(
            "/admin/login"
        )


    conn = get_db()


    conn.execute(
        """
        DELETE FROM questions
        WHERE id = ?
        """,

        (question_id,)

    )


    conn.commit()

    conn.close()


    return redirect("/admin")
@app.route("/admin/delete-all", methods=["POST"])
def delete_all_questions():
    try:
        conn = get_db()

        cursor = conn.cursor()

        cursor.execute("DELETE FROM questions")

        deleted_count = cursor.rowcount

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": f"{deleted_count} questions deleted successfully."
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin",
        None
    )


    return redirect("/")


# =========================================================
# START FLASK
# =========================================================

if __name__ == "__main__":

    # Initialize / upgrade database
    init_db()


    print("")
    print("======================================")
    print("       APTITUDE COACH")
    print("======================================")
    print("")
    print("Server running at:")
    print("http://127.0.0.1:5000")
    print("")
    print("Admin:")
    print("http://127.0.0.1:5000/admin/login")
    print("")
    print("Username: admin")
    print("Password: admin123")
    print("")
    print("======================================")
    print("")


    app.run(

        debug=True,

        host="127.0.0.1",

        port=5000

    )