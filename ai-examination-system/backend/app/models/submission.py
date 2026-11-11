import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Uuid, ForeignKey, DateTime, Numeric, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import SubmissionStatus


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    assignment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("examination_assignments.id"),
        nullable=False
    )
    status: Mapped[SubmissionStatus] = mapped_column(
        SQLEnum(SubmissionStatus, name="submission_status"),
        default=SubmissionStatus.PENDING
    )
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    total_marks: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))

    assignment: Mapped["ExaminationAssignment"] = relationship(
        back_populates="submissions"
    )
    answers: Mapped[list["StudentAnswer"]] = relationship(
        back_populates="submission",
        cascade="all, delete-orphan"
    )
    uploaded_files: Mapped[list["UploadedFile"]] = relationship(
        back_populates="submission",
        cascade="all, delete-orphan"
    )
    result: Mapped["ExaminationResult | None"] = relationship(
        back_populates="submission",
        cascade="all, delete-orphan",
        uselist=False
    )
