from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from database import get_db
from models import Session as SessionModel
from schemas import SessionCreate, SessionOut
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
)
# result = md.convert("document_with_images.pdf")
# print(result.text_content)

router = APIRouter(prefix="/session", tags=["sessions"])

@router.post("/", response_model=SessionOut)
def create_session(data: SessionCreate, db: DBSession = Depends(get_db)):
    new_session = SessionModel(
        student_name=data.student_name,
        essay_prompt=data.essay_prompt,
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


@router.get("/{id}", response_model=SessionOut)
def get_session(id: str, db: DBSession = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/{id}/essay", response_model=SessionOut)
def upload_essay(id: str, essay: str, db: DBSession = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.essay = essay
    db.commit()
    db.refresh(session)
    return session

#mainly for instructors 
@router.get("/", response_model=list[SessionOut])
def list_sessions(db: DBSession = Depends(get_db)):
    return db.query(SessionModel).all()


