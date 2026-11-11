
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import require_role
from app.database.session import get_db
from app.models.enums import UserRole
from app.models.examination import Examination
from app.models.examination_assignment import ExaminationAssignment
from app.models.user import User
from app.schemas.examination_assignment import (
    ExaminationAssignmentCreate,
    ExaminationAssignmentResponse
)

router = APIRouter(tags=["Examination Assignments"])


@router.post(
    "/api/examinations/{examination_id}/assignments/",
    response_model=ExaminationAssignmentResponse,
    status_code=status.HTTP_201_CREATED
)
def assign_examination(
    examination_id: uuid.UUID,
    assignment_data: ExaminationAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.TEACHER))
):
    examination = db.query(Examination).filter(
        Examination.id == examination_id,
        Examination.teacher_id == current_user.id
    ).first()

    if examination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Examination not found"
        )

    student = db.query(User).filter(
        User.id == assignment_data.student_id,
        User.role == UserRole.STUDENT
    ).first()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    existing_assignment = db.query(ExaminationAssignment).filter(
        ExaminationAssignment.examination_id == examination_id,
        ExaminationAssignment.student_id == student.id
    ).first()

    if existing_assignment:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Examination already assigned to this student"
        )

    assignment = ExaminationAssignment(
        examination_id=examination_id,
        student_id=student.id
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


@router.get(
    "/api/examinations/{examination_id}/assignments/",
    response_model=list[ExaminationAssignmentResponse]
)
def get_examination_assignments(
    examination_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.TEACHER))
):
    examination = db.query(Examination).filter(
        Examination.id == examination_id,
        Examination.teacher_id == current_user.id
    ).first()

    if examination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Examination not found"
        )

    return db.query(ExaminationAssignment).filter(
        ExaminationAssignment.examination_id == examination_id
    ).order_by(
        ExaminationAssignment.assigned_at.desc()
    ).all()


@router.delete(
    "/api/assignments/{assignment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_assignment(
    assignment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.TEACHER))
):
    assignment = db.query(ExaminationAssignment).join(
        Examination
    ).filter(
        ExaminationAssignment.id == assignment_id,
        Examination.teacher_id == current_user.id
    ).first()

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    db.delete(assignment)
    db.commit()
