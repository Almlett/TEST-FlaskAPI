import uuid
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas, worker
from app.database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.post("/api/tasks", response_model=schemas.TaskResponse, status_code=202)
def create_analysis_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
	if not task.text.strip():
		raise HTTPException(status_code=400, detail="Text cannot be empty")

	db_task = crud.create_task(db=db, task=task)
	worker.process_text_task.delay(str(db_task.id))
	return {"task_id":db_task.id}


@app.get("/api/tasks/{task_id}", response_model=schemas.TaskStatus)
def get_task_status(task_id: uuid.UUID, db: Session = Depends(get_db)):
	db_task = crud.get_task(db, task_id=task_id)
	if db_task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return db_task
