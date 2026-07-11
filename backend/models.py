from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Uuid, Integer
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
    phase = Column(String, default="thesis")

    prewriting_messages = relationship(
        "SessionMessage",
        back_populates="session",
        order_by="SessionMessage.created_at",

    )
    criterion_statuses = relationship("SessionCriterionStatus", back_populates="session")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    prompt = Column(Text)
    rubric_text = Column(Text)
    exemplar_text = Column(Text)
    target_audience = Column(String)
    genre = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    # good for the ai to know the exemplar annotations for grounding purposes
    exemplar_annotations = relationship("ExemplarAnnotation", back_populates="assignment")
    sessions = relationship("Session", back_populates="assignment")

    rubric_criteria = relationship(
        "RubricCriterion",
        back_populates="assignment",
        order_by="RubricCriterion.order",
    )


class ExemplarAnnotation(Base):
    __tablename__ = "exemplar_annotations"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    assignment_id = Column(Uuid, ForeignKey("assignments.id"), nullable=False)
    span_start = Column(String, nullable=False)
    span_end = Column(String, nullable=False)
    quote = Column(Text, nullable=False)
    comment_type = Column(String)   # content | genre | rhetorical | audience
    comment = Column(Text, nullable=False)
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
    created_at = Column(DateTime, default=datetime.now)

    session = relationship("Session", back_populates="annotations")
    messages = relationship(
        "AnnotationMessage",
        back_populates="annotation",
        order_by="AnnotationMessage.created_at",
    )


class AnnotationMessage(Base):
    __tablename__ = "annotation_messages"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    annotation_id = Column(Uuid, ForeignKey("student_annotations.id"), nullable=False)
    role = Column(String, nullable=False)     
    content = Column(Text, nullable=False)      
    created_at = Column(DateTime, default=datetime.now)

    annotation = relationship("StudentAnnotation", back_populates="messages")
    

class SessionMessage(Base):
    __tablename__ = "session_messages"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid, ForeignKey("sessions.id"), nullable=False)
    role = Column(String, nullable=False)      
    content = Column(Text, nullable=False)
    phase = Column(String, nullable=False)      # thesis | claims_evidence | rubric_alignment | wrap
    created_at = Column(DateTime, default=datetime.now)

    session = relationship("Session", back_populates="prewriting_messages")

class RubricCriterion(Base):
    __tablename__ = "rubric_criteria"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    assignment_id = Column(Uuid, ForeignKey("assignments.id"), nullable=False)
    criterion_text = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    updated_at = Column(DateTime, default=datetime.now)

    assignment = relationship("Assignment", back_populates="rubric_criteria")
    statuses = relationship("SessionCriterionStatus", back_populates="criterion") 

class SessionCriterionStatus(Base):
    __tablename__ = "session_criterion_statuses"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id = Column(Uuid, ForeignKey("sessions.id"), nullable=False)
    criterion_id = Column(Uuid, ForeignKey("rubric_criteria.id"), nullable=False)
    status = Column(String, nullable=False)     # not_started | in_progress | completed
    updated_at = Column(DateTime, default=datetime.now)

    session = relationship("Session", back_populates="criterion_statuses")
    criterion = relationship("RubricCriterion", back_populates="statuses")