# seed_frankenstein_rubric.py
from database import SessionLocal
from models import RubricCriterion, Assignment
import uuid

db = SessionLocal()
try:
    assignment_id = uuid.UUID("8cb6141c-6bb8-4af1-83f3-3926d29768ca")
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise ValueError("Assignment not found")

    db.query(RubricCriterion).filter(RubricCriterion.assignment_id == assignment_id).delete()

    criteria = [
        "Thesis: should state a clear, arguable position on how the novel "
        "critiques unchecked scientific ambition. (Weak version to flag: "
        "summarizing the plot instead of making a claim.)",

        "Evidence: claims should be backed by specific textual evidence, "
        "quotes or scenes from the novel. (Weak version to flag: vague "
        "references to 'the book' without specific moments.)",

        "Alternative interpretation: essay should acknowledge and respond "
        "to at least one other reasonable reading of the novel. (Weak "
        "version to flag: treating the thesis as the only possible reading.)",
    ]

    for i, text in enumerate(criteria, start=1):
        db.add(RubricCriterion(assignment_id=assignment.id, criterion_text=text, order=i))

    db.commit()
    print(f"Seeded {len(criteria)} criteria for assignment {assignment.id}")
finally:
    db.close()