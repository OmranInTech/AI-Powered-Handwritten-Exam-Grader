
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import require_role
from app.database.session import get_db
from app.models.enums import UserRole, ExamStatus
from app.models.examination import Examination
from app.models.user import User
from app.schemas.examination import (
    ExaminationCreate,
    ExaminationUpdate,
    ExaminationResponse
)

router = APIRouter(prefix="/api/examinations", tags=["Examinations"])


@router.post(
    "/",
    response_model=ExaminationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_examination(
    exam_data: ExaminationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.TEACHER))
):
    examination = Examination(
        **exam_data.model_dump(),
        teacher_id=current_user.id,
        status=ExamStatus.DRAFT
    )

    db.add(examination)
    db.commit()
    db.refresh(examination)

    return examination


@router.get("/", response_model=list[ExaminationResponse])
def get_examinations(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.TEACHER))
):
    return db.query(Examination).filter(
        Examination.teacher_id == current_user.id
    ).order_by(Examination.created_at.desc()).all()


@router.get("/{examination_id}", response_model=ExaminationResponse)
def get_examination(
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

    return examination


@router.patch("/{examination_id}", response_model=ExaminationResponse)
def update_examination(
    examination_id: uuid.UUID,
    exam_data: ExaminationUpdate,
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

    update_data = exam_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(examination, field, value)

    db.commit()
    db.refresh(examination)

    return examination


@router.delete("/{examination_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_examination(
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

    if examination.status != ExamStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft examinations can be deleted"
        )

    db.delete(examination)
    db.commit()
