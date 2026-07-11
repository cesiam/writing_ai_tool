from services.feedback import generate_feedback
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from database import get_db
import uuid
from schemas import AnnotationSpan, AnnotationOut

router = APIRouter()

@router.post("/sessions/{id}/feedback/generate", response_model=list[AnnotationOut])
def general_feedback_route(id: uuid.UUID, db: DBSession = Depends(get_db)):
    return generate_feedback(id, db)


