import uuid
from database import SessionLocal
from models import Assignment, Session

db = SessionLocal()

assignment_id = uuid.UUID("8cb6141c-6bb8-4af1-83f3-3926d29768ca") #Frankenstein id
session_ids = db.query(Session).filter(Session.assignment_id == assignment_id)
for session in session_ids:
    print(session.id)
db.close()