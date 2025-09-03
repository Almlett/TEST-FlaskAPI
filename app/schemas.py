# -*- coding: utf-8 -*-
from uuid import UUID

from pydantic import BaseModel


class TaskCreate(BaseModel):
	"""Schema for creating a new task.

	Attributes:
		text (str): The input text to be processed.
	"""
	text: str


class TaskResponse(BaseModel):
	"""Schema for the response after task creation.

	Attributes:
		task_id (UUID): The unique identifier of the created task.
	"""
	task_id: UUID


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

	class Config:
		"""Pydantic configuration options."""
		orm_mode = True

