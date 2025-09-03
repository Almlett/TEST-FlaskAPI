# -*- coding: utf-8 -*-
import logging
import time

from celery import Celery

from app import crud
from app.config import settings
from app.database import SessionLocal
from app.schemas import TaskStatusEnum

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_text_task(self, task_id: str):
    """Celery task to process text from a database record.

    This task fetches a task by its ID from the database, simulates a
    long-running text processing operation, calculates the word and character
    counts, and updates the task record with the result and a 'COMPLETED'
    status. If an error occurs, the task status is set to 'FAILED'.

    Args:
        task_id (str): The UUID of the task to process, passed as a string.
    """
    db = SessionLocal()
    task = None
    try:
        task = crud.get_task(db, task_id=task_id)
        if not task:
            logger.warning(f"Task with id {task_id} not found.")
            return

        task.status = TaskStatusEnum.IN_PROGRESS
        db.commit()

        # Simulate a long-running process
        time.sleep(15)

        text = task.text
        word_count = len(text.split())
        char_count = len(text)
        result_data = {"word_count": word_count, "char_count": char_count}

        task.status = TaskStatusEnum.COMPLETED
        task.result = result_data
        db.commit()

    except Exception as exc:
        logger.error(f"Error processing task {task_id}: {exc}", exc_info=True)
        if task:
            task.status = TaskStatusEnum.FAILED
            db.commit()
        # Retry the task if it's a transient error
        self.retry(exc=exc)
    finally:
        db.close()
