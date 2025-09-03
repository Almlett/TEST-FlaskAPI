# -*- coding: utf-8 -*-
import datetime
import uuid

from sqlalchemy import JSON, Column, DateTime, String, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from app.schemas import TaskStatusEnum

class Task(Base):
	"""A SQLAlchemy model representing a text processing task.

	This model stores information about a task, including the input text,
	its current status, the final result, and timestamps for tracking.

	Attributes:
		id (UUID): The primary key for the task, a universally unique identifier.
		text (str): The input text content that needs to be processed.
		status (str): The current status of the task (e.g., 'PENDING', 
			'PROCESSING', 'COMPLETED', 'FAILED'). Defaults to 'PENDING'.
		result (dict): A JSON field to store the outcome of the processing. 
			It is nullable and will be empty until the task is completed.
		created_at (datetime): The timestamp indicating when the task was created.
		updated_at (datetime): The timestamp of the last modification to the task.
			This is automatically updated on any change.
	"""
	__tablename__ = "tasks"
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	text = Column(String, nullable=False)
	status = Column(SQLAlchemyEnum(TaskStatusEnum), default=TaskStatusEnum.PENDING, nullable=False)
	result = Column(JSON, nullable=True)
	created_at = Column(DateTime, default=datetime.datetime.now)
	updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
