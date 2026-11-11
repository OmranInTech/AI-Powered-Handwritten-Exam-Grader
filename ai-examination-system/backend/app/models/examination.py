
import uuid

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.base import Base
from app.models.enums import ExamMode, GradingPolicy, ExamStatus


class Examination(Base):
    __tablename__ = "examinations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    teacher_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    mode: Mapped[ExamMode] = mapped_column(Enum(ExamMode, name="exam_mode"), nullable=False)
    grading_policy: Mapped[GradingPolicy] = mapped_column(Enum(GradingPolicy, name="grading_policy"), nullable=False)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    exam_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    status: Mapped[ExamStatus] = mapped_column(
        Enum(ExamStatus, name="exam_status"),
        nullable=False,
        default=ExamStatus.DRAFT
    )
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    teacher = relationship("User", back_populates="examinations")
    questions = relationship(
        "Question",
        back_populates="examination",
        cascade="all, delete-orphan"
    )
