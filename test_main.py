
from uuid import uuid4

from fastapi.testclient import TestClient

from main import app
from schemas import GradeRecordResponse

client = TestClient(app)


def test_grade_crud_and_duplicate_prevention():
    student_id = f"TEST{uuid4().hex[:10].upper()}"

    payload = {
        "student_id": student_id,
        "course_code": "PY101",
        "semester": "Semester 1",
        "score": 80,
    }

    try:
        # 1. Create a grade record
        response = client.post("/grades", json=payload)

        assert response.status_code == 201
        assert response.json()["score"] == 80
        assert response.json()["letter_grade"] == "B"

        # 2. Reject a duplicate record
        response = client.post("/grades", json=payload)

        assert response.status_code == 409

        # 3. Retrieve records
        response = client.get("/grades")

        assert response.status_code == 200
        assert any(
            item["student_id"] == student_id
            and item["course_code"] == "PY101"
            for item in response.json()
        )

        # 4. Update the score
        response = client.patch(
            f"/grades/{student_id}/PY101",
            json={"score": 95},
        )

        assert response.status_code == 200
        assert response.json()["score"] == 95
        assert response.json()["letter_grade"] == "A"

        # 5. Delete the record
        response = client.delete(
            f"/grades/{student_id}/PY101"
        )

        assert response.status_code == 200

        # 6. Verify deletion
        response = client.get("/grades")

        assert response.status_code == 200
        assert not any(
            item["student_id"] == student_id
            and item["course_code"] == "PY101"
            for item in response.json()
        )

    finally:
        # Clean up if the test fails before deletion.
        client.delete(f"/grades/{student_id}/PY101")


def test_rejects_invalid_score():
    payload = {
        "student_id": f"TEST{uuid4().hex[:10].upper()}",
        "course_code": "PY101",
        "semester": "Semester 1",
        "score": 150,
    }

    response = client.post("/grades", json=payload)

    assert response.status_code == 422


def test_rejects_negative_score():
    payload = {
        "student_id": f"TEST{uuid4().hex[:10].upper()}",
        "course_code": "PY101",
        "semester": "Semester 1",
        "score": -1,
    }

    response = client.post("/grades", json=payload)

    assert response.status_code == 422


def test_rejects_invalid_course_code():
    payload = {
        "student_id": f"TEST{uuid4().hex[:10].upper()}",
        "course_code": "py101",
        "semester": "Semester 1",
        "score": 80,
    }

    response = client.post("/grades", json=payload)

    assert response.status_code == 422


def test_update_missing_record():
    student_id = f"MISSING{uuid4().hex[:8].upper()}"

    response = client.patch(
        f"/grades/{student_id}/PY101",
        json={"score": 90},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Grade record not found"


def test_delete_missing_record():
    student_id = f"MISSING{uuid4().hex[:8].upper()}"

    response = client.delete(
        f"/grades/{student_id}/PY101"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Grade record not found"


def test_update_without_score():
    student_id = f"MISSING{uuid4().hex[:8].upper()}"

    response = client.patch(
        f"/grades/{student_id}/PY101",
        json={},
    )

    assert response.status_code == 404


def test_letter_grade_thresholds():
    test_cases = [
        (100, "A"),
        (90, "A"),
        (89, "B"),
        (75, "B"),
        (74, "C"),
        (50, "C"),
        (49, "F"),
        (0, "F"),
    ]

    for score, expected_grade in test_cases:
        record = GradeRecordResponse(
            student_id="TEST001",
            course_code="CS101",
            semester="Semester 1",
            score=score,
        )

        assert record.letter_grade == expected_grade


def test_update_schema_rejects_invalid_score():
    from pydantic import ValidationError
    from schemas import GradeRecordUpdate

    try:
        GradeRecordUpdate(score=101)
    except ValidationError:
        pass
    else:
        raise AssertionError("Expected invalid score to be rejected")


def test_update_schema_allows_missing_score():
    from schemas import GradeRecordUpdate

    update = GradeRecordUpdate()

    assert update.score is None
