import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session as DBSession
from database import get_db
from models import Assignment
from schemas import AssignmentCreate, AssignmentOut
import shutil, tempfile, os
from markitdown import MarkItDown

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

@router.get("/assignments", response_model=list[AssignmentOut])
def list_assignments(db: DBSession = Depends(get_db)):
    return db.query(Assignment).all()

md_converter = MarkItDown(enable_plugins=False)

@router.put("/assignments/{id}/rubric", response_model=AssignmentOut)
def upload_rubric(id: uuid.UUID, file: UploadFile, db: DBSession = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        result = md_converter.convert(tmp_path)
        assignment.rubric_text = result.text_content
    finally:
        os.remove(tmp_path)
    db.commit()
    db.refresh(assignment)
    return assignment