from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id        = Column(Integer, primary_key=True)
    email     = Column(String, unique=True, index=True)
    name      = Column(String)
    role      = Column(String, default="faculty")
    hashed_pw = Column(String)
    students  = relationship("Student", back_populates="teacher")

class Student(Base):
    __tablename__ = "students"
    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    teacher_id  = Column(Integer, ForeignKey("users.id"))
    risk_score  = Column(Float)
    risk_level  = Column(String)
    absences    = Column(Integer)
    studytime   = Column(Integer)
    failures    = Column(Integer)
    shap_json   = Column(String)
    created_at  = Column(DateTime, default=datetime.utcnow)
    teacher       = relationship("User", back_populates="students")
    interventions = relationship("Intervention", back_populates="student")

class Intervention(Base):
    __tablename__ = "interventions"
    id          = Column(Integer, primary_key=True)
    student_id  = Column(Integer, ForeignKey("students.id"))
    action      = Column(String)
    action_type = Column(String)
    priority    = Column(String)
    applied     = Column(Boolean, default=False)
    applied_at  = Column(DateTime, nullable=True)
    student     = relationship("Student", back_populates="interventions")