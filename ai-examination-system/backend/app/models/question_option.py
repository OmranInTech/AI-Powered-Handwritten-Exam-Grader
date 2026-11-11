import uuid

from sqlalchemy import Text, Boolean, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class QuestionOption(Base):
    __tablename__ = "question_options"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("questions.id"), nullable=False
    )
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

    question: Mapped["Question"] = relationship(back_populates="options")
