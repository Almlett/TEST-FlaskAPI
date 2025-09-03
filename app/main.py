# -*- coding: utf-8 -*-
import uuid

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, worker
from app.database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
	"""A generator function that serves as a dependency to provide a database session.

	This function is designed to be used as a dependency in a web framework like
	FastAPI. It creates a new SQLAlchemy `SessionLocal` instance for a single
	request-response cycle. It yields the session to be used within a path
	operation function or another dependency.

	The use of a `try...finally` block ensures that the database session is
	always closed after the request has been handled, regardless of whether
	an exception occurred during processing. This is a crucial pattern for
	managing database connections and preventing resource leaks.

	Yields:
		sqlalchemy.orm.Session: The database session object for the current context.
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.post("/api/v1/tasks", response_model=schemas.TaskResponse, status_code=202)
def create_analysis_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
	"""Create a new analysis task and enqueue it for processing.

	This endpoint receives text data, creates a corresponding task record
	in the database, and then adds the task to a background worker queue
	for asynchronous processing. It performs a basic validation to ensure
	the provided text is not empty.

	The endpoint immediately returns a 202 Accepted status code along with
	the task ID, indicating that the request has been accepted for processing,
	but the processing has not been completed.

	Args:
		task (schemas.TaskCreate): The request body containing the data for the
			new task, primarily the text to be analyzed.
		db (Session, optional): The database session dependency, injected by
			FastAPI. Defaults to Depends(get_db).

	Raises:
		HTTPException: Raised with a 400 status code if the `text` field in
			the task payload is empty or contains only whitespace.

	Returns:
		schemas.TaskResponse: A response object containing the ID of the newly
			created task.
	"""
	if not task.text.strip():
		raise HTTPException(status_code=400, detail="Text cannot be empty")
	db_task = crud.create_task(db=db, task=task)
	worker.process_text_task.delay(str(db_task.id))
	return {"task_id":db_task.id}


@app.get("/api/v1/tasks/{task_id}", response_model=schemas.TaskStatus)
def get_task_status(task_id: uuid.UUID, db: Session = Depends(get_db)):
	"""Retrieves a specific task from the database by its ID.

	This function fetches a task's details from the database using its unique
	identifier. If a task with the specified ID is found, the corresponding
	database object is returned. If no task is found, it raises an HTTP
	exception to indicate that the resource was not found.

	Args:
		task_id (uuid.UUID): The unique identifier of the task to retrieve.
		db (Session): The database session dependency, provided by FastAPI.

	Returns:
		The task object from the database that matches the provided task_id.

	Raises:
		HTTPException: A 404 Not Found error is raised if no task with the
			specified task_id exists in the database.
	"""
	db_task = crud.get_task(db, task_id=task_id)
	if db_task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return db_task
