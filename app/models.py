from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from .db import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

class Batch(Base):
    __tablename__ = "batches"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    course_id = Column(String, ForeignKey("courses.id"))
    created_at = Column(DateTime, server_default=func.now())

class LessonPlan(Base):
    __tablename__ = "lesson_plans"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    duration_mins = Column(Integer, nullable=False)
    markdown = Column(Text, nullable=False)
    content_json = Column(JSON)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    batch_id = Column(String, ForeignKey("batches.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(String, primary_key=True)
    lesson_plan_id = Column(String, ForeignKey("lesson_plans.id"), nullable=False)
    markdown = Column(Text, nullable=False)
    schema_json = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
