from pydantic import BaseModel
from uuid import UUID

class TaskCreate(BaseModel):
	text: str

class TaskResponse(BaseModel):
	task_id: UUID

class TaskStatus(BaseModel):
	id: UUID
	status: str
	result: dict | None=None

	class Config:
		orm_mode = True
