
import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import QuestionType


class QuestionOptionCreate(BaseModel):
    option_text: str = Field(min_length=1)
    is_correct: bool = False


class QuestionCreate(BaseModel):
    question_text: str = Field(min_length=1)
    question_type: QuestionType
    marks: Decimal = Field(gt=0)
    reference_answer: str | None = None
    position: int | None = Field(default=None, ge=1)
    options: list[QuestionOptionCreate] = []


class QuestionOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    option_text: str
    is_correct: bool


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    examination_id: uuid.UUID
    question_text: str
    question_type: QuestionType
    marks: Decimal
    reference_answer: str | None
    position: int | None
    options: list[QuestionOptionResponse] = []
