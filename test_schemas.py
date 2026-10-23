from schemas import (
    GradeRecordCreate,
    GradeRecordUpdate,
    GradeRecordResponse,
)

# Test creation
record = GradeRecordCreate(
    student_id="STU101",
    course_code="CS101",
    semester="Semester 1",
    score=85.5,
)
print(record)

# Test update
update = GradeRecordUpdate(score=90)
print(update)

# Test calculated grade
response = GradeRecordResponse(
    student_id="STU101",
    course_code="CS101",
    semester="Semester 1",
    score=95,
)
print(response.model_dump())

from pydantic import ValidationError

# Test invalid course code
try:
    GradeRecordCreate(
        student_id="STU101",
        course_code="cs101",
        semester="Semester 1",
        score=85,
    )
except ValidationError as error:
    print("Invalid course code rejected")
    print(error)

# Test invalid score
try:
    GradeRecordCreate(
        student_id="STU101",
        course_code="CS101",
        semester="Semester 1",
        score=105,
    )
except ValidationError as error:
    print("Invalid score rejected")
    print(error)

# Test omitted update score
update = GradeRecordUpdate()
print("Omitted score:", update.score)

# Test 1: Valid score update
update1 = GradeRecordUpdate(score=88)
print("Valid update:", update1)

# Test 2: Update without a score
update2 = GradeRecordUpdate()
print("Empty update:", update2)

# Test 3: Invalid score update
try:
    GradeRecordUpdate(score=120)
except Exception as e:
    print("Invalid update rejected:", e)