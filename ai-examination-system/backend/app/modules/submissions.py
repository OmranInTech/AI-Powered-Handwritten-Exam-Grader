
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.enums import UserRole, SubmissionStatus
from app.models.examination_assignment import ExaminationAssignment
from app.models.submission import Submission
from app.models.user import User
from app.schemas.submission import SubmissionResponse

router = APIRouter(tags=["Submissions"])


@router.post(
    "/api/assignments/{assignment_id}/submissions/",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_submission(
    assignment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can create submissions"
        )

    assignment = db.query(ExaminationAssignment).filter(
        ExaminationAssignment.id == assignment_id,
        ExaminationAssignment.student_id == current_user.id
    ).first()

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Examination assignment not found"
        )

    existing_submission = db.query(Submission).filter(
        Submission.assignment_id == assignment_id
    ).first()

    if existing_submission:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Submission already exists"
        )

    submission = Submission(
        assignment_id=assignment_id,
        status=SubmissionStatus.PENDING
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)

    return submission


@router.get(
    "/api/submissions/{submission_id}",
    response_model=SubmissionResponse
)
def get_submission(
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

    return submission
