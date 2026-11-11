import uuid
from datetime import datetime

from sqlalchemy import Uuid, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ExaminationAssignment(Base):
    __tablename__ = "examination_assignments"

    __table_args__ = (
        UniqueConstraint(
            "examination_id",
            "student_id",
            name="uq_exam_student_assignment"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    examination_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("examinations.id"),
        nullable=False
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    examination: Mapped["Examination"] = relationship()
    student: Mapped["User"] = relationship()
    submissions: Mapped[list["Submission"]] = relationship(
        back_populates="assignment",
        cascade="all, delete-orphan"
    )
