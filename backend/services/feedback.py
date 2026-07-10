import typing
import uuid
from sqlalchemy.orm import Session
from schemas import FeedbackOutput, AnnotationSpan
from services.ai_client import call_model
from models import Session as SessionModel
from models import StudentAnnotation, AnnotationMessage
from sqlalchemy.orm import Session as DBSession

FEEDBACK_SYSTEM_PROMPT = """
You are giving feedback on a student's essay draft for a writing-intensive class.

Your feedback must help the student meet the requirements in the rubric provided.
Ground every comment in a specific rubric requirement or gap; do not give generic
writing advice unrelated to the rubric or the assignment's audience/genre.

For each issue you notice, classify it under exactly one of these four lenses:
- content: is the claim well-supported? is the reasoning sound? is evidence used well?
- genre: does this follow the conventions of the assigned document type? is it
  recognizable as that type of writing?
- rhetorical: is the purpose clear? is the evidence and reasoning suited to that purpose?
- audience: will the intended reader follow this? does it serve or alienate them?

For each span you flag:
- quote the exact text from the essay (verbatim, so it can be located)
- assign one comment_type from the four above
- write a brief comment naming the issue
- write a question that prompts the student to reconsider that part themselves

Critical rules:
- Never rewrite or supply replacement sentences. Only point and ask.
- Do not give a holistic verdict on the whole essay; only span-level comments.
- Ground each comment in the rubric, not personal stylistic preference.
- Return only the structured output in the required schema, nothing else.
"""

def generate_feedback(session_id: uuid.UUID, db: DBSession) -> list[StudentAnnotation]:
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    assignment = session.assignment

    messages = [
        {"role": "system", "content": FEEDBACK_SYSTEM_PROMPT},
        {"role": "user", "content": f"Rubric:\n{assignment.rubric_text}\n\nEssay:\n{session.student_essay}"}
    ]

    result = call_model(messages, FeedbackOutput) 
    annotations = []

    for span in result.annotations:  
        annotation = StudentAnnotation(
            session_id=session_id,
            span_start=span.span_start,
            span_end=span.span_end,
            quote=span.quote,
            comment_type=span.comment_type,
        )
        db.add(annotation)
        db.flush()  

        message_content = span.comment
        if span.question:
            message_content += f" {span.question}"

        db.add(AnnotationMessage(
            annotation_id=annotation.id,
            role="ai",
            content=message_content,
        ))
        annotations.append(annotation)
    db.commit()
    return annotations