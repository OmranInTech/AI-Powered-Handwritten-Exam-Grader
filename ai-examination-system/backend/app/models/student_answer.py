import uuid
from decimal import Decimal

from sqlalchemy import Uuid, ForeignKey, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class StudentAnswer(Base):
    __tablename__ = "student_answers"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    submission_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("submissions.id"),
        nullable=False
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("questions.id"),
        nullable=False
    )
    answer_text: Mapped[str | None] = mapped_column(Text)
    selected_option_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("question_options.id")
    )
    awarded_marks: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))

    submission: Mapped["Submission"] = relationship(back_populates="answers")
    question: Mapped["Question"] = relationship()
    selected_option: Mapped["QuestionOption | None"] = relationship()
    ai_evaluations: Mapped[list["AIEvaluation"]] = relationship(
        back_populates="student_answer",
        cascade="all, delete-orphan"
    )
