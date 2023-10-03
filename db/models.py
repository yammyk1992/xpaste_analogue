import uuid

from sqlalchemy import UUID, Column, String

from db.database import Base


class Text(Base):
    __tablename__ = "text_create"

    text_uuid = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    text = Column(String(255), nullable=False)
    salt = Column(String, nullable=False)
