from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_generate_feedback():
    
    assignment_resp = client.post("/assignments", json={
        "name": "WWI Essay",
        "prompt": "Discuss the causes of WWI",
        "rubric_text": "The essay must state a clear thesis, support claims with specific "
                        "evidence, and organize paragraphs around distinct causes."
    })
    print("ASSIGNMENT:", assignment_resp.status_code, assignment_resp.json())
    assert assignment_resp.status_code == 200
    assignment_id = assignment_resp.json()["id"]

    
    session_resp = client.post("/session", json={
        "student_name": "Test Student",
        "essay_prompt": "Discuss the causes of WWI",
        "assignment_id": assignment_id
    })
    print("SESSION:", session_resp.status_code, session_resp.json())
    assert session_resp.status_code == 200
    session_id = session_resp.json()["id"]

    
    with open("test_files/sample_essay.docx", "rb") as f:
        upload_resp = client.put(
            f"/session/{session_id}/essay",
            files={"file": ("sample_essay.docx", f,
                   "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
    print("UPLOAD:", upload_resp.status_code, upload_resp.json())
    assert upload_resp.status_code == 200
    assert upload_resp.json()["student_essay"] != ""

    
    feedback_resp = client.post(f"/sessions/{session_id}/feedback/generate")
    print("FEEDBACK:", feedback_resp.status_code, feedback_resp.json())
    assert feedback_resp.status_code == 200

    annotations = feedback_resp.json()
    assert isinstance(annotations, list)
    assert len(annotations) > 0
    first = annotations[0]
    assert "quote" in first
    assert "comment_type" in first
    assert "comment" in first
    assert first["comment_type"] in ("content", "genre", "rhetorical", "audience")