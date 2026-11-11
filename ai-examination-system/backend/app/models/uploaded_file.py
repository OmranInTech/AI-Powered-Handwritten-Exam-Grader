import uuid
from datetime import datetime

from sqlalchemy import Uuid, ForeignKey, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    submission_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("submissions.id"),
        nullable=False
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    submission: Mapped["Submission"] = relationship(
        back_populates="uploaded_files"
    )
