from fastapi import FastAPI

from app.services.task import TaskService
from app.worker.worker import app as worker_app
from app.api.routes.api import r

app = FastAPI()
app.include_router(r)
app.state.task_service = TaskService(app=worker_app)
