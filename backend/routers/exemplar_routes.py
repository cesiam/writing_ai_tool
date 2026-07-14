import uuid
import shutil
import tempfile
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session as DBSession
from database import get_db
from models import Assignment, ExemplarAnnotation
from schemas import ExemplarAnnotationCreate, ExemplarAnnotationOut, AssignmentOut
from markitdown import MarkItDown

md_converter = MarkItDown(enable_plugins=False)

router = APIRouter()


@router.put("/assignments/{id}/exemplar", response_model=AssignmentOut)
def upload_exemplar(id: uuid.UUID, file: UploadFile, db: DBSession = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        result = md_converter.convert(tmp_path)
        text = result.text_content
    finally:
        os.remove(tmp_path)

    assignment.exemplar_text = text
    db.commit()
    db.refresh(assignment)
    return assignment


@router.get("/assignments/{id}/exemplar-annotations", response_model=list[ExemplarAnnotationOut])
def list_exemplar_annotations(id: uuid.UUID, db: DBSession = Depends(get_db)):
    return (
        db.query(ExemplarAnnotation)
        .filter(ExemplarAnnotation.assignment_id == id)
        .order_by(ExemplarAnnotation.span_start)
        .all()
    )


@router.post("/assignments/{id}/exemplar-annotations", response_model=ExemplarAnnotationOut)
def create_exemplar_annotation(id: uuid.UUID, data: ExemplarAnnotationCreate, db: DBSession = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    annotation = ExemplarAnnotation(
        assignment_id=id,
        span_start=data.span_start,
        span_end=data.span_end,
        quote=data.quote,
        comment_type=data.comment_type,
        comment=data.comment,
    )
    db.add(annotation)
    db.commit()
    db.refresh(annotation)
    return annotation


@router.delete("/exemplar-annotations/{annotation_id}")
def delete_exemplar_annotation(annotation_id: uuid.UUID, db: DBSession = Depends(get_db)):
    annotation = db.query(ExemplarAnnotation).filter(ExemplarAnnotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    db.delete(annotation)
    db.commit()
    return {"deleted": True}
