from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import Base
import datetime

class Task(Base):
	__tablename__ = "tasks"
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	text = Column(String, nullable=False)
	status = Column(String, default="PENDING")
	result = Column(JSON, nullable=True)
	created_at = Column(DateTime, default=datetime.datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

