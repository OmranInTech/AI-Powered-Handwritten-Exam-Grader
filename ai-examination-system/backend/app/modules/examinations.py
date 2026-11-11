
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.permissions import require_role
from app.database.session import get_db
from app.models.enums import UserRole, ExamStatus
from app.models.examination import Examination
from app.models.user import User
from app.schemas.examination import (
    ExaminationCreate,
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
