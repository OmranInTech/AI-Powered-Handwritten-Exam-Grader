import uuid
from decimal import Decimal

from sqlalchemy import Text, Numeric, Integer, Enum as SQLEnum, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import QuestionType


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    examination_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("examinations.id"), nullable=False
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(
        SQLEnum(QuestionType, name="question_type"), nullable=False
    )
    marks: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    reference_answer: Mapped[str | None] = mapped_column(Text)
    position: Mapped[int | None] = mapped_column(Integer)

    examination: Mapped["Examination"] = relationship(back_populates="questions")
    options: Mapped[list["QuestionOption"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )

