
from fastapi import FastAPI
from sqlalchemy import text
from app.modules.questions import router as question_router
from app.database.session import engine
from app.modules.auth import router as auth_router
from app.modules.examinations import router as examination_router
from app.modules.assignments import router as assignment_router
from app.modules.submissions import router as submission_router
from app.modules.uploads import router as upload_router
from app.modules.answers import router as answer_router


app = FastAPI(
    title="AI Examination System API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(examination_router)
app.include_router(question_router)
app.include_router(assignment_router)
app.include_router(submission_router)
app.include_router(upload_router)
app.include_router(answer_router)

@app.get("/")
def root():
    return {"message": "AI Examination System API is running"}


@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}
