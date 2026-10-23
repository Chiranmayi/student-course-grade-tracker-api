
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
)


# 1. Calculate the letter grade
def calculate_grade(score: float) -> str:
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "F"


# 2. Schema for creating a grade record
class GradeRecordCreate(BaseModel):
    student_id: str
    course_code: str = Field(
        pattern=r"^[A-Z]{2,4}[0-9]{3}$"
    )
    semester: str
    score: float = Field(ge=0, le=100)

    @field_validator("course_code")
    @classmethod
    def validate_course_code(cls, value: str) -> str:
        if value != value.upper():
            raise ValueError(
                "Course code must use uppercase letters"
            )
        return value

    @field_validator("score")
    @classmethod
    def validate_score_thresholds(cls, value: float) -> float:
        if not 0 <= value <= 100:
            raise ValueError(
                "Score must be between 0 and 100"
            )
        return value


# 3. Schema for updating a grade record
class GradeRecordUpdate(BaseModel):
    score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )


# 4. Schema for the response
class GradeRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: str
    course_code: str
    semester: str
    score: float

    @computed_field
    @property
    def letter_grade(self) -> str:
        return calculate_grade(self.score)
