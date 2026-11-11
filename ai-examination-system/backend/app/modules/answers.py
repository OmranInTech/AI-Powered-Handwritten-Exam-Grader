
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.enums import UserRole, SubmissionStatus
from app.models.examination_assignment import ExaminationAssignment
from app.models.submission import Submission
from app.models.student_answer import StudentAnswer
from app.models.question import Question
from app.models.user import User
from app.schemas.student_answer import (
    StudentAnswerCreate,
    StudentAnswerResponse
)

router = APIRouter(tags=["Student Answers"])


@router.post(
    "/api/submissions/{submission_id}/answers/",
    response_model=StudentAnswerResponse,
    status_code=status.HTTP_201_CREATED
)
def create_answer(
    submission_id: uuid.UUID,
    answer_data: StudentAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).join(
        ExaminationAssignment
    ).filter(
        Submission.id == submission_id,
        ExaminationAssignment.student_id == current_user.id
    ).first()

    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )

    if submission.status != SubmissionStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submission is no longer accepting answers"
        )

    question = db.query(Question).filter(
        Question.id == answer_data.question_id,
        Question.examination_id == ExaminationAssignment.examination_id
    ).join(
        ExaminationAssignment,
        ExaminationAssignment.examination_id == Question.examination_id
    ).filter(
        ExaminationAssignment.id == submission.assignment_id
    ).first()

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found in this examination"
        )

    existing_answer = db.query(StudentAnswer).filter(
        StudentAnswer.submission_id == submission_id,
        StudentAnswer.question_id == answer_data.question_id
    ).first()

    if existing_answer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Answer already exists for this question"
        )

    answer = StudentAnswer(
        submission_id=submission_id,
        **answer_data.model_dump()
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)

    return answer


@router.get(
    "/api/submissions/{submission_id}/answers/",
    response_model=list[StudentAnswerResponse]
)
def get_submission_answers(
    submission_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submission = db.query(Submission).join(
        ExaminationAssignment
    ).filter(
        Submission.id == submission_id,
        ExaminationAssignment.student_id == current_user.id
    ).first()

    if submission is None and current_user.role == UserRole.TEACHER:
        from app.models.examination import Examination

        submission = db.query(Submission).join(
            ExaminationAssignment
        ).join(
            Examination
        ).filter(
            Submission.id == submission_id,
            Examination.teacher_id == current_user.id
        ).first()

    if submission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )

    return db.query(StudentAnswer).filter(
        StudentAnswer.submission_id == submission_id
    ).all()
