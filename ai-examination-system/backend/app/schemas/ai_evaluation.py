
import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AIEvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    student_answer_id: uuid.UUID
    suggested_marks: Decimal | None
    feedback: str | None
    model_name: str | None
    created_at: datetime
