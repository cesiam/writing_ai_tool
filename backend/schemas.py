import pydantic as py
from uuid import UUID

class SessionCreate(py.BaseModel):
    student_name: str
    essay_prompt: str

class SessionOut(py.BaseModel):
    id: UUID
    student_name: str
    essay_prompt: str
    created_at: datetime
    updated_at: datetime