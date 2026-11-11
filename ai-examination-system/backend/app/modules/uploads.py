
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.enums import UserRole
from app.models.examination import Examination
from app.models.examination_assignment import ExaminationAssignment
from app.models.submission import Submission
from app.models.uploaded_file import UploadedFile
from app.models.user import User
from app.schemas.uploaded_file import UploadedFileResponse

router = APIRouter(tags=["File Uploads"])

STORAGE_DIR = Path("../storage/submissions").resolve()
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}
MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post(
    "/api/submissions/{submission_id}/upload/",
    response_model=UploadedFileResponse,
    status_code=status.HTTP_201_CREATED
)
def upload_examination_file(
    submission_id: uuid.UUID,
    file: UploadFile = File(...),
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

    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, PNG, and JPEG files are allowed"
        )

    content = file.file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty"
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size cannot exceed 20 MB"
        )

    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    stored_name = f"{uuid.uuid4()}{extension}"
    file_path = STORAGE_DIR / stored_name

    file_path.write_bytes(content)

    uploaded_file = UploadedFile(
        submission_id=submission.id,
        file_name=Path(file.filename).name,
        file_path=str(file_path),
        file_type=extension.lstrip(".")
    )

    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)

    return uploaded_file
