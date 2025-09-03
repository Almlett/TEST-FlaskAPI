# -*- coding: utf-8 -*-
import uuid

from sqlalchemy.orm import Session

from app import models, schemas

def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
	"""Creates a new task and saves it to the database.

	This function takes a database session and a task creation schema as input.
	It creates a new `Task` model instance, adds it to the session, commits
	the transaction to persist it in the database, and then refreshes the
	instance to load any database-generated values (e.g., the primary key).

	Args:
		db (Session): The SQLAlchemy database session for database operations.
		task (schemas.TaskCreate): A Pydantic schema containing the data for the
			new task, such as the task's text content.

	Returns:
		models.Task: The newly created and persisted Task model instance,
			refreshed with its state from the database.
	"""
	db_task = models.Task(text=task.text)
	db.add(db_task)
	db.commit()
	db.refresh(db_task)
	return db_task

def get_task(db: Session, task_id: uuid.UUID):
	"""Retrieves a single task from the database by its unique identifier.

	Args:
		db (Session): The SQLAlchemy database session for database communication.
		task_id (uuid.UUID): The unique identifier of the task to fetch.

	Returns:
		models.Task | None: The `Task` model instance if a task with the
							specified ID is found, otherwise `None`.
	"""
	return db.query(models.Task).filter(models.Task.id == task_id).first()
