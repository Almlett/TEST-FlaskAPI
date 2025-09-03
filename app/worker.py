from celery import Celery
import time
from .database import SessionLocal
from . import models

celery_app = Celery(
	"worker",
	broker="redis://redis:6379/0",
	backend="redis://redis:6379/0"
)

@celery_app.task
def process_text_task(task_id: str):
	db = SessionLocal()
	try:
		task = db.query(models.Task).filter(models.Task.id == task_id).first()
		if not task:
			return

		task.status = "IN_PROGRESS"
		db.commit()

		time.sleep(15)

		text = task.text
		word_count = len(text.split())
		char_count = len(text)
		result_data = {"word_count": word_count, "char_count": char_count}

		task.status  ="COMPLETED"
		task.result = result_data
		db.commit()

	except Exception as e:
		task.status = "Failed"
		db.commit()
	finally:
		db.close()
