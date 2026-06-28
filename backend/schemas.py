from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class SessionCreate(BaseModel):
    student_name: str
    essay_prompt: str

class SessionOut(BaseModel):
    id: UUID
    student_name: str
    essay_prompt: str
    student_essay: str
    created_at: datetime
    updated_at: datetime