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

class AnnotationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    session_id: UUID
    span_start: int
    span_end: int
    quote: str
    comment_type: Literal["content", "genre", "rhetorical", "audience"]
    comment: str
    question: str | None = None
    rationale: str | None = None

class FeedbackOutput(BaseModel):
    annotations: list[AnnotationSpan]

class PrewritingReply(BaseModel):
    reply: str
    phase: Literal["orient", "explore", "rubric_check", "wrap"]
    ready_to_wrap: bool

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
    created_at: datetime