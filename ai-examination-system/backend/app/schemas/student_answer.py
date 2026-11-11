
import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class StudentAnswerCreate(BaseModel):
    question_id: uuid.UUID
    answer_text: str | None = None
    selected_option_id: uuid.UUID | None = None


class StudentAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    submission_id: uuid.UUID
    question_id: uuid.UUID
    answer_text: str | None
    selected_option_id: uuid.UUID | None
    awarded_marks: Decimal | None
