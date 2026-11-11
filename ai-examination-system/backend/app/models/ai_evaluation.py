import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Uuid, ForeignKey, Numeric, Text, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AIEvaluation(Base):
    __tablename__ = "ai_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    student_answer_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("student_answers.id"),
        nullable=False
    )
    suggested_marks: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    feedback: Mapped[str | None] = mapped_column(Text)
    model_name: Mapped[str | None] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    student_answer: Mapped["StudentAnswer"] = relationship(
        back_populates="ai_evaluations"
    )
