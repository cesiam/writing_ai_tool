from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Literal


class SessionCreate(BaseModel):
    student_name: str
    essay_prompt: str
    assignment_id: UUID | None = None

class SessionOut(BaseModel):
    id: UUID
    student_name: str
    essay_prompt: str
    student_essay: str
    created_at: datetime
    updated_at: datetime

class AnnotationSpan(BaseModel):

    span_start: int
    span_end: int
    quote: str
    comment_type: Literal["content", "genre", "rhetorical", "audience"]
    comment: str
    question: str | None = None
    rationale: str | None = None


class AnnotationMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    role: Literal["ai", "student"]
    content: str
    created_at: datetime


class AnnotationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    session_id: UUID
    span_start: int
    span_end: int
    quote: str
    comment_type: Literal["content", "genre", "rhetorical", "audience"]
    created_at: datetime
    messages: list[AnnotationMessageOut] = []
    exemplar_text: str | None = None

class FeedbackOutput(BaseModel):
    annotations: list[AnnotationSpan]

class PrewritingReply(BaseModel):
    reply: str
    phase: Literal["thesis", "claims_evidence", "rubric_alignment", "wrap"]
    ready_to_advance: bool
    criteria_touched: list[UUID] = []

class AssignmentCreate(BaseModel):
    name: str
    prompt: str | None = None
    rubric_text: str | None = None

class AssignmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    prompt: str | None
    rubric_text: str | None
    exemplar_text: str | None = None
    created_at: datetime
    
class SessionMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    role: Literal["ai", "student"]
    content: str
    phase: Literal["thesis", "claims_evidence", "rubric_alignment", "wrap"]
    created_at: datetime

class PrewritingMessageIn(BaseModel):
    content: str

class AnnotationMessageIn(BaseModel):
    content: str

class AnnotationReply(BaseModel):
    content: str

class ExemplarAnnotationCreate(BaseModel):
    span_start: int
    span_end: int
    quote: str
    comment_type: Literal["content", "genre", "rhetorical", "audience"]
    comment: str

class ExemplarAnnotationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    assignment_id: UUID
    span_start: int
    span_end: int
    quote: str
    comment_type: Literal["content", "genre", "rhetorical", "audience"]
    comment: str
    created_at: datetime