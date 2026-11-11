
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExaminationAssignmentCreate(BaseModel):
    student_id: uuid.UUID


class ExaminationAssignmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    examination_id: uuid.UUID
    student_id: uuid.UUID
    assigned_at: datetime
