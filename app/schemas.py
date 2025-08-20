from pydantic import BaseModel
from typing import Optional, List, Any

class LessonReq(BaseModel):
    textContent: str
    studyDurationWeeks: int
    numStudents: int
    sectionsPerWeek: int
    courseId: str
    batchId: str
    title: Optional[str] = None
    topic: Optional[str] = None
    durationMins: Optional[int] = 40

class AssessReq(BaseModel):
    lessonPlanId: str
    textContent: str
    assessmentTypes: List[str] = []
    mcq_count: int = 0
    short_count: int = 0
    include_project: bool = False
    difficulty: str = "Intermediate"
    include_answers: bool = True
    project_focus: str = ""
    rubric_detail_level: str = "Detailed"

class PlanOut(BaseModel):
    id: str
    title: str
    topic: str
    durationMins: int
    markdown: str
    courseId: str
    batchId: str

class AssessmentOut(BaseModel):
    id: str
    lessonPlanId: str
    markdown: str
