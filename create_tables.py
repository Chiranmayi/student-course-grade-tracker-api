
from database import Base, engine
from models import GradeRecord

Base.metadata.create_all(bind=engine)

print("Grade tables created successfully!")
