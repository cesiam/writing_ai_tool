from database import SessionLocal, Base, engine
from models import RubricCriterion, Assignment

Base.metadata.create_all(bind=engine)

db = SessionLocal()

assignment = db.query(Assignment).filter(Assignment.name == "WWI Essay").first()
if not assignment:
    raise ValueError("Assignment not found, check the name")

criteria = [
    "Thesis: should be a clear, arguable, well-developed, definitive statement "
    "of position that answers a why or how question. (Weak version to flag: "
    "an outline of points that isn't actually arguable.)",

    "Development: paper should demonstrate logical, mature, thorough development "
    "of points that support the thesis. (Weak version to flag: superficial "
    "development, points that don't support the thesis.)",

    "Evidence, Analysis, Synthesis: should present relevant, fully analyzed "
    "textual evidence supporting the thesis, and synthesize evidence back to "
    "the thesis. (Weak version to flag: irrelevant or unanalyzed evidence, "
    "no attempt at synthesis.)",

    "Opposition/Refutation: should clearly explain the opposition and "
    "persuasively refute it. (Weak version to flag: opposition/refutation "
    "missing entirely.)",
]

for i, text in enumerate(criteria, start=1):
    db.add(RubricCriterion(
        assignment_id=assignment.id,
        criterion_text=text,
        order=i,
    ))

db.commit()
print(f"Seeded {len(criteria)} criteria for assignment {assignment.id}")