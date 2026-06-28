from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_essay():
    create_resp = client.post("/session", json={
        "student_name": "Test Student",
        "essay_prompt": "Discuss the causes of WWI"
    })
    print(create_resp.status_code, create_resp.json())
    session_id = create_resp.json()["id"]

    with open("test_files/sample_essay.docx", "rb") as f:
        response = client.put(
            f"/session/{session_id}/essay",
            files={"file": ("sample_essay.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
    print("UPLOAD:", response.status_code, response.json()) 
    assert response.status_code == 200
    assert response.json()["student_essay"] != ""