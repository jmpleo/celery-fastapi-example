from fastapi import APIRouter, Depends

from app.services.task import TaskService
from app.api.depends import get_task_service
from app.schemas.response import Response


r = APIRouter()


@r.get("/{task_id}", response_model=Response)
async def task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
    include_result: bool = True
) -> Response:
    task = await task_service.get_task(task_id, include_result)
    if not task:
        return Response(error='not started before')
    return Response(data=task)


@r.get("", response_model=Response)
async def tasks(
    task_service: TaskService = Depends(get_task_service)
) -> Response:
    tasks = await task_service.get_tasks()
    return Response(data=tasks)
