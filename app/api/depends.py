from fastapi import Request
from app.services.task import TaskService


def get_task_service(request: Request) -> TaskService:
    return request.app.state.task_service
