import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from database import get_db
from models import Assignment
from schemas import AssignmentCreate, AssignmentOut

router = APIRouter()

@router.post("/assignments", response_model=AssignmentOut)
def create_assignment(data: AssignmentCreate, db: DBSession = Depends(get_db)):
    assignment = Assignment(
        name=data.name,
        prompt=data.prompt,
        rubric_text=data.rubric_text
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment