# routers/prewriting_routes.py
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from pydantic import BaseModel

from database import get_db
from schemas import PrewritingReply, PrewritingMessageIn, SessionMessageOut
from services.prewriting import generate_prewriting_reply
from models import Session as SessionModel, SessionMessage

router = APIRouter()



@router.post("/sessions/{id}/prewriting/messages", response_model=PrewritingReply)
def post_prewriting_message(id: uuid.UUID, body: PrewritingMessageIn, db: DBSession = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return generate_prewriting_reply(id, body.content, db)


@router.get("/sessions/{id}/prewriting/messages", response_model=list[SessionMessageOut])
def get_prewriting_messages(id: uuid.UUID, db: DBSession = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = (
        db.query(SessionMessage)
        .filter(SessionMessage.session_id == id)
        .order_by(SessionMessage.created_at)
        .all()
    )
    return messages