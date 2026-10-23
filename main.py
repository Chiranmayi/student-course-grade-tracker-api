
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import GradeRecord
from schemas import (
    GradeRecordCreate,
    GradeRecordUpdate,
    GradeRecordResponse,
)

app = FastAPI()


# 1. Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Grade Tracker API"}


# 2. Create a grade record
@app.post(
    "/grades",
    response_model=GradeRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_grade(
    record: GradeRecordCreate,
    db: Session = Depends(get_db),
):
    # Check for an existing record for the same student,
    # course, and semester.
    existing_record = (
        db.query(GradeRecord)
        .filter(
            GradeRecord.student_id == record.student_id,
            GradeRecord.course_code == record.course_code,
            GradeRecord.semester == record.semester,
        )
        .first()
    )

    # Reject duplicate records
    if existing_record is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "This student already has a record "
                "for this course and semester"
            ),
        )

    # Create a new grade record
    db_record = GradeRecord(
        student_id=record.student_id,
        course_code=record.course_code,
        semester=record.semester,
        score=record.score,
    )

    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return db_record


# 3. Retrieve all grade records
@app.get(
    "/grades",
    response_model=list[GradeRecordResponse],
)
def get_grades(db: Session = Depends(get_db)):
    return db.query(GradeRecord).all()


# 4. Update a student's score
@app.patch(
    "/grades/{student_id}/{course_code}",
    response_model=GradeRecordResponse,
)
def update_grade(
    student_id: str,
    course_code: str,
    update: GradeRecordUpdate,
    db: Session = Depends(get_db),
):
    record = (
        db.query(GradeRecord)
        .filter(
            GradeRecord.student_id == student_id,
            GradeRecord.course_code == course_code,
        )
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade record not found",
        )

    if update.score is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a score to update",
        )

    record.score = update.score

    db.commit()
    db.refresh(record)

    return record


# 5. Delete a grade record
@app.delete("/grades/{student_id}/{course_code}")
def delete_grade(
    student_id: str,
    course_code: str,
    db: Session = Depends(get_db),
):
    record = (
        db.query(GradeRecord)
        .filter(
            GradeRecord.student_id == student_id,
            GradeRecord.course_code == course_code,
        )
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade record not found",
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Grade record deleted successfully"
    }
