import sqlalchemy as sa
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import uuid

class Session(Base):
    __tablename__ = "sessions"
    id = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String, index=True)
    description = sa.Column(sa.String, index=True)
    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, default=datetime.now)
