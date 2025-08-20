import io, os, uuid
from dotenv import load_dotenv
load_dotenv()  # will read .env or .env.local in project root
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pypdf import PdfReader
from .ai import make_client, model_id
from .db import Base, engine, get_db
from .models import LessonPlan, Assessment
from .schemas import LessonReq, AssessReq, PlanOut, AssessmentOut

# Create tables on first run (simple MVP). For prod use Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
origins = (os.getenv("ALLOWED_ORIGINS") or "").split(",")
if not any(origins):
    origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    """Upload a PDF and get back its text."""
    content = await file.read()
    reader = PdfReader(io.BytesIO(content))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return {"text": text}

@app.post("/lesson", response_model=dict)
def lesson(req: LessonReq, db: Session = Depends(get_db)):
    client = make_client()
    prompt = f"""
You are an expert pedagogy designer. Create a practical, well-structured lesson plan series.

Constraints:
- Weeks: {req.studyDurationWeeks}
- Students: {req.numStudents}
- Sections/week: {req.sectionsPerWeek}

Source:
---
{req.textContent[:6000]}
---

Requirements:
- Overview with goals/success criteria
- Weekly breakdown with objectives, topics, vocab
- For each section: teacher-led, student-centered, collaborative activities; materials; differentiation; assessment
- Homework/extension; enrichment
- Use Markdown headings + bullet points
"""
    r = client.chat.completions.create(
        model=model_id(),
        messages=[
            {"role": "system", "content": "You are a senior instructional designer and master teacher."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1200,
        temperature=0.4,
    )
    markdown = r.choices[0].message.content or ""
    plan = LessonPlan(
        id=str(uuid.uuid4()),
        title=req.title or f"{req.topic or 'Lesson'} — Plan",
        topic=req.topic or "General",
        duration_mins=req.durationMins or 40,
        markdown=markdown,
        course_id=req.courseId,
        batch_id=req.batchId,
    )
    db.add(plan)
    db.commit()
    return {"plan": {
        "id": plan.id,
        "title": plan.title,
        "topic": plan.topic,
        "durationMins": plan.duration_mins,
        "markdown": plan.markdown,
        "courseId": plan.course_id,
        "batchId": plan.batch_id,
    }}

@app.post("/assessments", response_model=dict)
def assessments(req: AssessReq, db: Session = Depends(get_db)):
    parts = []
    if "MCQ" in req.assessmentTypes and req.mcq_count > 0:
        parts.append(f"- MCQs: {req.mcq_count} questions with 4 options; difficulty {req.difficulty}.")
    if "Short Answer" in req.assessmentTypes and req.short_count > 0:
        parts.append(f"- Short Answer: {req.short_count} prompts at {req.difficulty}.")
    if req.include_project and "Project" in req.assessmentTypes:
        parts.append(f"- Project: focus '{req.project_focus or 'core objectives'}'; {req.rubric_detail_level.lower()} rubric.")
    include_key = "Include answer keys." if req.include_answers else "Do not include answer keys."

    prompt = f"""
You are an experienced assessment designer.

Specs:
{chr(10).join(parts) if parts else "- Propose a balanced set."}
Formatting: Markdown headings + bullets. {include_key}

Source:
---
{req.textContent[:6000]}
---
"""
    client = make_client()
    r = client.chat.completions.create(
        model=model_id(),
        messages=[
            {"role": "system", "content": "You write clear, fair, curriculum-aligned assessments."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1200,
        temperature=0.5,
    )
    markdown = r.choices[0].message.content or ""
    a = Assessment(
        id=str(uuid.uuid4()),
        lesson_plan_id=req.lessonPlanId,
        markdown=markdown,
    )
    db.add(a)
    db.commit()
    return {"assessment": {
        "id": a.id,
        "lessonPlanId": a.lesson_plan_id,
        "markdown": a.markdown,
    }}
