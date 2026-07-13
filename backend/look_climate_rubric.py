from database import SessionLocal
from models import RubricCriterion, Assignment
import uuid

db = SessionLocal()
try:
    assignment_id = uuid.UUID("36bf08bc-6eda-4be9-b2fd-e35f4cd710b1")
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise ValueError("Assignment not found")

    criteria = [
        "Position: should state a clear, arguable stance on whether the state "
        "should adopt a carbon tax. (Weak version to flag: hedging without "
        "taking an actual position, or a position that isn't really debatable.)",

        "Evidence: claims should be backed by specific data, studies, or "
        "concrete examples, not vague generalizations. (Weak version to flag: "
        "unsupported assertions, 'many people think' style claims.)",

        "Counterargument: essay should identify and respond to at least one "
        "reasonable objection to the student's position. (Weak version to "
        "flag: no acknowledgment that anyone might disagree.)",
    ]

    for i, text in enumerate(criteria, start=1):
        db.add(RubricCriterion(assignment_id=assignment.id, criterion_text=text, order=i))

    db.commit()
    print(f"Seeded {len(criteria)} criteria for assignment {assignment.id} for session {assignment.sessions[0].id}")
finally:
    db.close()