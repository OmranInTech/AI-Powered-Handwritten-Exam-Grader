
import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ExamMode, GradingPolicy, ExamStatus


class ExaminationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    subject: str = Field(min_length=1, max_length=150)
    description: str | None = None
    mode: ExamMode
    grading_policy: GradingPolicy
    duration_minutes: int | None = Field(default=None, gt=0)
    total_marks: Decimal = Field(gt=0)
    exam_date: date | None = None


class ExaminationUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    subject: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    mode: ExamMode | None = None
    grading_policy: GradingPolicy | None = None
    duration_minutes: int | None = Field(default=None, gt=0)
    total_marks: Decimal | None = Field(default=None, gt=0)
    exam_date: date | None = None
    status: ExamStatus | None = None


class ExaminationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    teacher_id: uuid.UUID
    title: str
    subject: str
    description: str | None
    mode: ExamMode
    grading_policy: GradingPolicy
    duration_minutes: int | None
    total_marks: Decimal
    exam_date: date | None
    status: ExamStatus
    created_at: datetime
