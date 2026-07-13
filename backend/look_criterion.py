from database import SessionLocal
from models import RubricCriterion
import uuid

db = SessionLocal()
rows = db.query(RubricCriterion).filter(
    RubricCriterion.assignment_id == uuid.UUID("36bf08bc-6eda-4be9-b2fd-e35f4cd710b1")
).all()
for r in rows:
    print(r.order, "|", r.criterion_text[:60])
db.close()