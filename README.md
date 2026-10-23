# Student Course Grade Tracker API

## Project Overview

The Student Course Grade Tracker API is a REST API built with Python, FastAPI, Pydantic, SQLAlchemy, and PostgreSQL. It manages student course grade records, validates input data, and calculates letter grades automatically.

## Features

- Create student grade records.
- Retrieve all grade records.
- Update a student's score.
- Delete a grade record.
- Validate course codes using regular expressions.
- Validate scores between 0 and 100.
- Calculate letter grades automatically.
- Prevent duplicate records for the same student, course, and semester.
- Store records in PostgreSQL.
- Run automated tests with pytest.

## Technologies Used

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Pytest
- HTTPX

## Letter Grade Rules

| Score    | Grade |
| -------- | ----- |
| 90–100   | A     |
| 75–89.99 | B     |
| 50–74.99 | C     |
| Below 50 | F     |

## Setup Instructions

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install fastapi uvicorn sqlalchemy "psycopg[binary]" pydantic pytest httpx
```

### 3. Configure PostgreSQL

Create a PostgreSQL database named `grade_tracker`.

Configure the database connection in `database.py` using your local PostgreSQL username, password, host, port, and database name.

Do not commit real passwords or other secrets to version control.

### 4. Create the database table

```powershell
python create_tables.py
```

### 5. Start the API

```powershell
python -m uvicorn main:app --reload
```

### 6. Open API documentation

Visit:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint                             | Purpose               |
| ------ | ------------------------------------ | --------------------- |
| GET    | `/`                                  | Welcome message       |
| POST   | `/grades`                            | Create a grade record |
| GET    | `/grades`                            | Retrieve all records  |
| PATCH  | `/grades/{student_id}/{course_code}` | Update a score        |
| DELETE | `/grades/{student_id}/{course_code}` | Delete a record       |

## Run Automated Tests

Run:

```powershell
python -m pytest -v
```

The tests cover CRUD operations, duplicate prevention, invalid inputs, missing records, optional updates, and letter-grade calculations.

## Learning Outcomes

- Pydantic schema design and validation.
- Regular expression validation.
- Numeric range validation.
- Custom field validators.
- Computed fields.
- FastAPI route development.
- SQLAlchemy ORM and PostgreSQL integration.
- Automated API testing with pytest.
