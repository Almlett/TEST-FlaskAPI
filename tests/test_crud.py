# -*- coding: utf-8 -*-
import uuid

from app import crud, schemas


def test_create_task(db_session):
	"""Test creating a task in the database."""
	task_schema = schemas.TaskCreate(text="Test CRUD task")
	db_task = crud.create_task(db=db_session, task=task_schema)
	assert db_task.text == "Test CRUD task"
	assert db_task.id is not None


def test_get_task(db_session):
	"""Test getting a task from the database."""
	task_schema = schemas.TaskCreate(text="Another CRUD task")
	db_task = crud.create_task(db=db_session, task=task_schema)
	retrieved_task = crud.get_task(db=db_session, task_id=db_task.id)
	assert retrieved_task
	assert retrieved_task.id == db_task.id
	assert retrieved_task.text == db_task.text


def test_get_nonexistent_task(db_session):
	"""Test getting a task that does not exist."""
	non_existent_uuid = uuid.uuid4()
	retrieved_task = crud.get_task(db=db_session, task_id=non_existent_uuid)
	assert retrieved_task is None
