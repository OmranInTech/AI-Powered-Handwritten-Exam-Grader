import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Uuid, ForeignKey, Numeric, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ExaminationResult(Base):
    __tablename__ = "examination_results"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    submission_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("submissions.id"),
        unique=True,
        nullable=False
    )
    total_marks: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    submission: Mapped["Submission"] = relationship(back_populates="result")
