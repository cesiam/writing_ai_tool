import sqlalchemy as sa
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import uuid

class Session(Base):
    __tablename__ = "sessions"
    id = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    student_name = sa.Column(sa.String, index=True)
    student_essay = sa.Column(sa.String, default="")
    essay_prompt = sa.Column(sa.String, index=True)
    updated_at = sa.Column(sa.DateTime, default=datetime.now)
    created_at = sa.Column(sa.DateTime, default=datetime.now)
