# -*- coding: utf-8 -*-
from unittest.mock import patch

from fastapi.testclient import TestClient

from app import schemas


def test_create_task_success(test_client: TestClient):
	"""Test creating a task successfully."""
	with patch("app.worker.process_text_task.delay") as mock_task:
		response = test_client.post("/api/v1/tasks", json={"text": "Test task"})
		assert response.status_code == 202
		data = response.json()
		assert "task_id" in data
		mock_task.assert_called_once()


def test_create_task_empty_text(test_client: TestClient):
	"""Test creating a task with empty text."""
	response = test_client.post("/api/v1/tasks", json={"text": " "})
	assert response.status_code == 400
	assert response.json() == {"detail": "Text cannot be empty"}


def test_get_task_not_found(test_client: TestClient):
	"""Test getting a task that does not exist."""
	response = test_client.get("/api/v1/tasks/00000000-0000-0000-0000-000000000000")
	assert response.status_code == 404
	assert response.json() == {"detail": "Task not found"}


def test_get_task_success(test_client: TestClient, db_session):
	"""Test getting a task successfully."""
	# Create a task first
	task_text = "A task to be found"
	response = test_client.post("/api/v1/tasks", json={"text": task_text})
	assert response.status_code == 202
	task_id = response.json()["task_id"]

	# Now get the task
	response = test_client.get(f"/api/v1/tasks/{task_id}")
	assert response.status_code == 200
	task = schemas.TaskStatus.model_validate(response.json())
	assert str(task.id) == task_id
	assert task.status == "PENDING"
