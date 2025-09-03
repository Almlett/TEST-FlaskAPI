from sqlalchemy.orm import Session
from .import models, schemas
import uuid

def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
	db_task = models.Task(text=task.text)
	db.add(db_task)
	db.commit()
	db.refresh(db_task)
	return db_task

def get_task(db: Session, task_id: uuid.UUID):
	return db.query(models.Task).filter(models.Task.id == task_id).first()
