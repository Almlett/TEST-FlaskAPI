# -*- coding: utf-8 -*-
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class TaskStatusEnum(str, Enum):
	"""An enumeration for the possible statuses of a task.

	Attributes:
		PENDING (str): The task has been created but has not yet started.
		IN_PROGRESS (str): The task is currently being executed.
		COMPLETED (str): The task has finished successfully.
		FAILED (str): The task has failed during execution.
	"""
	PENDING = "PENDING"
	IN_PROGRESS = "IN_PROGRESS"
	COMPLETED = "COMPLETED"
	FAILED = "FAILED"


class TaskBase(BaseModel):
	"""Base schema for a task, defining the core field."""

	text: str = Field(..., min_length=1, description="The text content of the task.")


class TaskCreate(TaskBase):
	"""Schema for creating a new task. Inherits from TaskBase."""

	pass


class TaskResponse(BaseModel):
	"""Schema for the response after task creation.

	Attributes:
		task_id (UUID): The unique identifier of the created task.
	"""
	task_id: UUID


class Task(BaseModel):
	"""Schema for a task as stored in the database, including its ID."""

	id: UUID
	model_config = ConfigDict(from_attributes=True)


class TaskStatus(BaseModel):
	"""Schema for representing the status and result of a task.

	Attributes:
		id (UUID): The unique identifier of the task.
		status (str): The current status of the task (e.g., 'PENDING', 'COMPLETED').
		result (dict | None): The processing result, which is None until the task is completed.
	"""
	id: UUID
	status: str
	result: dict | None = None
	model_config = ConfigDict(from_attributes=True)

