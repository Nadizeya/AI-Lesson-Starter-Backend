📚 AI Lesson Planner – Backend (FastAPI)
This is the backend service for the AI-powered Lesson Planner.
It provides APIs for generating, storing, and retrieving lesson plans (via OpenAI), and will later support assessments & analytics.

🚀 Features

Lesson Plan Generation → Upload content or text, generate a structured plan with AI.

CRUD API for Lesson Plans → create, list, get, update, delete.

PDF Extraction → extract text from uploaded lesson slides.

Database (Postgres) → stores courses, batches, and lesson plans.

FastAPI → modern Python web framework with auto docs at /docs.

🗂️ Project Structure
backend/
  app/
    ├── __init__.py
    ├── main.py          # FastAPI app + routers
    ├── db.py            # SQLAlchemy engine/session
    ├── models.py        # Database models
    ├── schemas.py       # Pydantic schemas
    ├── ai.py            # OpenAI client wrapper
    └── routers/         # API endpoints
        ├── health.py
        ├── extract.py
        ├── lesson.py
        └── plans.py
  .env                   # environment variables (not committed)
  .env.example           # safe template for env vars
  requirements.txt
  README.md

⚙️ Setup & Installation
1. Clone the repo
git clone https://github.com/your-username/ai-lesson-planner-backend.git
cd ai-lesson-planner-backend

2. Create a virtual environment
python -m venv .venv


Activate:

Windows (PowerShell)

.venv\Scripts\Activate.ps1


Mac/Linux

source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Create your .env
cp .env.example .env


Fill in your real values:

DATABASE_URL=postgresql://postgres:password@localhost:5432/lesson_planner
OPENAI_API_KEY=sk-xxxxxxx
OPENAI_MODEL=gpt-5-chat-latest
ALLOWED_ORIGINS=http://localhost:3000

5. Run the server
uvicorn app.main:app --reload


Backend is live at:
👉 http://127.0.0.1:8000

Interactive API docs:
👉 http://127.0.0.1:8000/docs

🧪 Example API Calls

Health check

curl http://127.0.0.1:8000/health


Generate Lesson Plan

curl -X POST http://127.0.0.1:8000/lesson \
  -H "Content-Type: application/json" \
  -d '{
    "textContent": "Hello curriculum...",
    "studyDurationWeeks": 6,
    "numStudents": 30,
    "sectionsPerWeek": 2,
    "courseId": "course-1",
    "batchId": "batch-A",
    "topic": "Linear Equations",
    "durationMins": 40
  }'


List Plans

curl http://127.0.0.1:8000/plans

🗄️ Database

Uses Postgres.

You must create lesson_planner DB first:

createdb lesson_planner


SQLAlchemy auto-creates tables at startup.

Seed example course/batch (if needed):

INSERT INTO courses (id, name) VALUES ('course-1', 'Demo Course');
INSERT INTO batches (id, name, course_id) VALUES ('batch-A', 'Batch A', 'course-1');

📜 License

MIT License © 2025


 Lesson Plan generation

 Assessments (quiz, MCQs)

 Student response collection

 Analytics dashboard
