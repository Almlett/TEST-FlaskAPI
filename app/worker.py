# -*- coding: utf-8 -*-
import time

from celery import Celery

from app import models
from app.database import SessionLocal

celery_app = Celery(
	"worker",
	broker="redis://redis:6379/0",
	backend="redis://redis:6379/0"
)


@celery_app.task
def process_text_task(task_id: str):
	"""Celery task to process text from a database record.

	This task fetches a task by its ID from the database, simulates a
	long-running text processing operation, calculates the word and character
	counts, and updates the task record with the result and a 'COMPLETED'
	status. If an error occurs, the task status is set to 'FAILED'.

	Args:
		task_id (str): The UUID of the task to process, passed as a string.
	"""
	db = SessionLocal()
	try:
		task = db.query(models.Task).filter(models.Task.id == task_id).first()
		if not task:
			return

		task.status = "IN_PROGRESS"
		db.commit()

		# Simulate a long-running process
		time.sleep(15)

		text = task.text
		word_count = len(text.split())
		char_count = len(text)
		result_data = {"word_count": word_count, "char_count": char_count}

		task.status = "COMPLETED"
		task.result = result_data
		db.commit()

	except Exception:
		if task:
			task.status = "FAILED"
			db.commit()
	finally:
		db.close()
