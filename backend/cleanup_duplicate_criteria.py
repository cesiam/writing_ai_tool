# cleanup_duplicate_criteria.py
from database import SessionLocal
from models import RubricCriterion
import uuid

db = SessionLocal()
try:
    assignment_id = uuid.UUID("36bf08bc-6eda-4be9-b2fd-e35f4cd710b1")
    rows = (
        db.query(RubricCriterion)
        .filter(RubricCriterion.assignment_id == assignment_id)
        .order_by(RubricCriterion.order, RubricCriterion.criterion_text)
        .all()
    )

    seen_orders = set()
    deleted = 0
    for row in rows:
        if row.order in seen_orders:
            db.delete(row)
            deleted += 1
        else:
            seen_orders.add(row.order)

    db.commit()
    print(f"Deleted {deleted} duplicate rows, kept {len(seen_orders)} unique criteria")
finally:
    db.close()