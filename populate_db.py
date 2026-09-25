import sqlite3
import os
import json
import re
from google import genai

# ============================================================
# CONFIGURATION
# ============================================================

DB_NAME = "aptitude.db"

MODEL_NAME = "gemini-3.1-flash-lite"


# ============================================================
# GEMINI SETUP
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set.\n"
        "Set it using:\n"
        '$env:GEMINI_API_KEY="YOUR_API_KEY"'
    )

client = genai.Client(api_key=API_KEY)


# ============================================================
# DATABASE
# ============================================================

def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
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
    conn.close()


# ============================================================
# GENERATE QUESTIONS
# ============================================================

def generate_questions(
    category,
    topic,
    difficulty,
    company,
    number
):

    prompt = f"""
You are an expert aptitude question creator.

Generate EXACTLY {number} UNIQUE aptitude questions.

Category: {category}
Topic: {topic}
Difficulty: {difficulty}
Company: {company}

These questions are for students preparing for placement exams.

IMPORTANT RULES:

1. Generate exactly {number} questions.
2. Every question must have exactly 4 options.
3. Only ONE option can be correct.
4. The answer must be exactly one of:
   A
   B
   C
   D
5. Give a clear explanation.
6. Questions must be mathematically or logically correct.
7. Do not create duplicate questions.
8. Match the requested difficulty.
9. Keep questions suitable for placement preparation.
10. Do not use markdown.
11. Do not use ``` or code blocks.
12. Return ONLY valid JSON.
13. Return a JSON ARRAY.
14. Do not add any text before or after the JSON.

Use exactly this format:

[
  {{
    "question": "Question text",
    "option_a": "Option A",
    "option_b": "Option B",
    "option_c": "Option C",
    "option_d": "Option D",
    "answer": "A",
    "explanation": "Explanation",
    "category": "{category}",
    "topic": "{topic}",
    "difficulty": "{difficulty}",
    "company": "{company}"
  }}
]
"""

    print("\nGenerating questions using Gemini...")
    print("-" * 60)
    print(f"Category  : {category}")
    print(f"Topic     : {topic}")
    print(f"Difficulty: {difficulty}")
    print(f"Company   : {company}")
    print(f"Number    : {number}")
    print("-" * 60)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    text = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    text = text.strip()

    # ========================================================
    # PARSE JSON
    # ========================================================

    try:
        questions = json.loads(text)

    except json.JSONDecodeError:

        print("\nGemini returned invalid JSON:")
        print("-" * 60)
        print(text)
        print("-" * 60)

        raise ValueError(
            "Gemini response could not be converted into JSON."
        )

    if not isinstance(questions, list):
        raise ValueError(
            "Gemini response is not a JSON array."
        )

    return questions


# ============================================================
# VALIDATE QUESTIONS
# ============================================================

def validate_question(q):

    required_fields = [
        "question",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "answer",
        "explanation",
        "category",
        "topic",
        "difficulty",
        "company"
    ]

    # Check fields
    for field in required_fields:

        if field not in q:
            print(f"Missing field: {field}")
            return False

        if q[field] is None:
            print(f"Empty field: {field}")
            return False

        if str(q[field]).strip() == "":
            print(f"Empty field: {field}")
            return False

    # Check answer
    answer = str(q["answer"]).strip().upper()

    if answer not in ["A", "B", "C", "D"]:
        print(f"Invalid answer: {answer}")
        return False

    return True


# ============================================================
# INSERT QUESTIONS
# ============================================================

def insert_questions(questions):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    inserted = 0

    for index, q in enumerate(questions, start=1):

        print(f"\nProcessing question {index}...")

        if not isinstance(q, dict):
            print("Skipped: question is not a JSON object.")
            continue

        if not validate_question(q):
            print("Skipped: validation failed.")
            continue

        answer = str(q["answer"]).strip().upper()

        cursor.execute("""
            INSERT INTO questions (

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

            str(q["question"]).strip(),

            str(q["option_a"]).strip(),

            str(q["option_b"]).strip(),

            str(q["option_c"]).strip(),

            str(q["option_d"]).strip(),

            answer,

            str(q["explanation"]).strip(),

            str(q["category"]).strip(),

            str(q["topic"]).strip(),

            str(q["difficulty"]).strip(),

            str(q["company"]).strip(),

            1,  # Show in Quiz

            1   # Show in Learn Topics

        ))

        inserted += 1

        print("Inserted successfully.")

    conn.commit()
    conn.close()

    return inserted


# ============================================================
# MAIN MENU
# ============================================================

def main():

    print("=" * 60)
    print("        APTITUDE COACH - GEMINI DATABASE POPULATOR")
    print("=" * 60)

    create_database()

    # ========================================================
    # CATEGORY
    # ========================================================

    print("\nSelect Category:")

    print("1. Quantitative Aptitude")
    print("2. Logical Reasoning")
    print("3. Verbal Ability")
    print("4. Data Interpretation")

    category_choice = input(
        "\nEnter choice: "
    ).strip()

    categories = {

        "1": "Quantitative Aptitude",

        "2": "Logical Reasoning",

        "3": "Verbal Ability",

        "4": "Data Interpretation"

    }

    category = categories.get(
        category_choice,
        "Quantitative Aptitude"
    )

    # ========================================================
    # TOPIC
    # ========================================================

    topic = input(
        "\nEnter Topic "
        "(Example: Percentages, Profit and Loss, Time and Work): "
    ).strip()

    if not topic:
        topic = "General"

    # ========================================================
    # DIFFICULTY
    # ========================================================

    print("\nSelect Difficulty:")

    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    difficulty_choice = input(
        "\nEnter choice: "
    ).strip()

    difficulties = {

        "1": "Easy",

        "2": "Medium",

        "3": "Hard"

    }

    difficulty = difficulties.get(
        difficulty_choice,
        "Easy"
    )

    # ========================================================
    # COMPANY
    # ========================================================

    company = input(
        "\nCompany "
        "(Example: TCS, Infosys, Zoho, Google, General): "
    ).strip()

    if not company:
        company = "General"

    # ========================================================
    # NUMBER OF QUESTIONS
    # ========================================================

    number_input = input(
        "\nHow many questions should be generated? "
    ).strip()

    try:

        number = int(number_input)

    except ValueError:

        print("Invalid number. Using 10 questions.")

        number = 10

    if number <= 0:

        print("Number must be greater than 0.")

        number = 10

    # ========================================================
    # GENERATE
    # ========================================================

    questions = generate_questions(

        category=category,

        topic=topic,

        difficulty=difficulty,

        company=company,

        number=number

    )

    print("\n" + "=" * 60)

    print(
        f"Gemini generated {len(questions)} questions."
    )

    print("=" * 60)

    # ========================================================
    # INSERT
    # ========================================================

    inserted = insert_questions(questions)

    # ========================================================
    # RESULT
    # ========================================================

    print("\n" + "=" * 60)
    print("DATABASE UPDATE COMPLETE")
    print("=" * 60)

    print(
        f"Questions generated : {len(questions)}"
    )

    print(
        f"Questions inserted  : {inserted}"
    )

    print(
        f"Database            : {DB_NAME}"
    )

    print("\nQuestions are now available in your Flask app.")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()