
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    String, Text, Integer, Date, DateTime, Numeric,
    Enum as SQLEnum, Uuid, ForeignKey, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import ExamMode, GradingPolicy, ExamStatus


class Examination(Base):
    __tablename__ = "examinations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    mode: Mapped[ExamMode] = mapped_column(
        SQLEnum(ExamMode, name="exam_mode"), nullable=False
    )
    grading_policy: Mapped[GradingPolicy] = mapped_column(
        SQLEnum(GradingPolicy, name="grading_policy"), nullable=False
    )
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    total_marks: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    exam_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[ExamStatus] = mapped_column(
        SQLEnum(ExamStatus, name="exam_status"),
        default=ExamStatus.DRAFT
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    teacher: Mapped["User"] = relationship(back_populates="examinations")
    questions: Mapped[list["Question"]] = relationship(
        back_populates="examination",
        cascade="all, delete-orphan"
    )
