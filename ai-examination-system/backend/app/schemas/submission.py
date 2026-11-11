
import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.enums import SubmissionStatus


class SubmissionCreate(BaseModel):
    assignment_id: uuid.UUID


class SubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    assignment_id: uuid.UUID
    status: SubmissionStatus
    submitted_at: datetime | None
    total_marks: Decimal | None
