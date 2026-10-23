
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Connect to the PostgreSQL database
DATABASE_URL = "postgresql+psycopg://postgres:post123@localhost:5432/grade_tracker"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


# Provide a database session to API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
