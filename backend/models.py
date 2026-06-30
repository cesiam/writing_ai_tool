from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import uuid

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    student_name = Column(String, index=True)
    student_essay = Column(String, default="")
    essay_prompt = Column(String, index=True)
    updated_at = Column(DateTime, default=datetime.now)
    created_at = Column(DateTime, default=datetime.now)
    assignment_id = Column(Uuid, ForeignKey("assignments.id"), nullable=True)   
    assignment = relationship("Assignment", back_populates="sessions")          
    annotations = relationship("StudentAnnotation", back_populates="session")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    prompt = Column(Text)
    rubric_text = Column(Text)
    exemplar_text = Column(Text)
    general_comments = Column(Text)
    target_audience = Column(String)
    genre = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    # good for the ai to know the exemplar annotations for grounding purposes
    exemplar_annotations = relationship("ExemplarAnnotation", back_populates="assignment")
    sessions = relationship("Session", back_populates="assignment")


class ExemplarAnnotation(Base):
    __tablename__ = "exemplar_annotations"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    assignment_id = Column(Uuid, ForeignKey("assignments.id"), nullable=False)
    span_start = Column(String, nullable=False)   # the string denotes an int
    span_end = Column(String, nullable=False) # the string denotes an int
    quote = Column(Text, nullable=False)
    comment_type = Column(String)   # content | genre | rhetorical | audience
    comment = Column(Text, nullable=False)
    parent_id = Column(Uuid, ForeignKey("exemplar_annotations.id"), nullable=True)
    status = Column(String, default="suggested")  # suggested | accepted | edited | rejected
    created_at = Column(DateTime, default=datetime.now)

    assignment = relationship("Assignment", back_populates="exemplar_annotations")


class StudentAnnotation(Base):
    __tablename__ = "student_annotations"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid, ForeignKey("sessions.id"), nullable=False)
    span_start = Column(String, nullable=False)
    span_end = Column(String, nullable=False)
    quote = Column(Text, nullable=False)
    comment_type = Column(String)
    comment = Column(Text, nullable=False)
    question = Column(Text)
    rationale = Column(Text)   
    created_at = Column(DateTime, default=datetime.now)

    session = relationship("Session", back_populates="annotations")
    messages = relationship("AnnotationMessage", back_populates="annotation")


class AnnotationMessage(Base):
    __tablename__ = "annotation_messages"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    annotation_id = Column(Uuid, ForeignKey("student_annotations.id"), nullable=False)
    role = Column(String, nullable=False)   
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    annotation = relationship("StudentAnnotation", back_populates="messages")
    

