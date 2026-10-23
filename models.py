
from sqlalchemy import Column, Integer, String, Float
from database import Base


class GradeRecord(Base):
    __tablename__ = "grade_records"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, nullable=False, index=True)
    course_code = Column(String, nullable=False, index=True)
    semester = Column(String, nullable=False)
    score = Column(Float, nullable=False)
