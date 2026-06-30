from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session as DBSession
from database import get_db
from models import Session as SessionModel
from schemas import SessionCreate, SessionOut
from markitdown import MarkItDown
import shutil, tempfile, os
import uuid
from datetime import datetime

md_converter = MarkItDown(
    enable_plugins=False
)


router = APIRouter(prefix="/session", tags=["sessions"])

@router.post("/", response_model=SessionOut)
def create_session(data: SessionCreate, db: DBSession = Depends(get_db)):
    new_session = SessionModel(
        student_name=data.student_name,
        essay_prompt=data.essay_prompt,
        assignment_id=data.assignment_id,   
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
def upload_essay(id: uuid.UUID, file: UploadFile, db: DBSession = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        result = md_converter.convert(tmp_path)
        text = result.text_content
    finally:
        os.remove(tmp_path)
    session.student_essay = text
    session.updated_at = datetime.now()
    db.commit()
    db.refresh(session)
    return session

#mainly for instructors 
@router.get("/", response_model=list[SessionOut])
def list_sessions(db: DBSession = Depends(get_db)):
    return db.query(SessionModel).all()


