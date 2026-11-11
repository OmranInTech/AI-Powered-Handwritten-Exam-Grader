
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UploadedFileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    submission_id: uuid.UUID
    file_name: str
    file_path: str
    file_type: str
    uploaded_at: datetime
