import uuid
from sqlalchemy.orm import Session as DBSession
from schemas import AnnotationReply
from services.ai_client import call_model
from models import StudentAnnotation, AnnotationMessage

ANNOTATION_REPLY_SYSTEM_PROMPT = """
You are continuing a Socratic conversation with a student about one specific
part of their essay. The flagged text is:

"{quote}"

This was flagged under the "{comment_type}" lens. Continue the conversation
naturally based on what the student just said. Ask follow-up questions that
help them reconsider or strengthen this part of their writing. Never rewrite
their sentence for them or give them exact replacement text, only ask
questions and point out gaps in their reasoning.

Respond with your reply text only, in the content field.
"""


def generate_annotation_reply(annotation_id: uuid.UUID, student_message: str, db: DBSession) -> AnnotationMessage:
    annotation = db.query(StudentAnnotation).filter(StudentAnnotation.id == annotation_id).first()
    if not annotation:
        raise ValueError("Annotation not found")

    db.add(AnnotationMessage(
        annotation_id=annotation_id,
        role="student",
        content=student_message,
    ))
    db.flush()

    thread = (
        db.query(AnnotationMessage)
        .filter(AnnotationMessage.annotation_id == annotation_id)
        .order_by(AnnotationMessage.created_at)
        .all()
    )

    system_prompt = ANNOTATION_REPLY_SYSTEM_PROMPT.format(
        quote=annotation.quote,
        comment_type=annotation.comment_type,
    )
    messages = [{"role": "system", "content": system_prompt}]
    for m in thread:
        role = "assistant" if m.role == "ai" else "user"
        messages.append({"role": role, "content": m.content})

    result = call_model(messages, AnnotationReply)

    ai_message = AnnotationMessage(
        annotation_id=annotation_id,
        role="ai",
        content=result.content,
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)
    return ai_message