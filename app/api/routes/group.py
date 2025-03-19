from fastapi import APIRouter, Depends

from app.services.task import TaskService
from app.api.depends import get_task_service
from app.schemas.response import Response


r = APIRouter()


@r.get("/{group_id}", response_model=Response)
async def group(
    group_id: str,
    task_service: TaskService = Depends(get_task_service),
    include_result: bool = True
) -> Response:
    group = await task_service.get_group(group_id, include_result)
    if not group:
        return Response(error='not started before')
    return Response(data=group)


@r.get("", response_model=Response)
async def groups(
    task_service: TaskService = Depends(get_task_service)
) -> Response:
    groups = await task_service.get_groups()
    return Response(data=groups)
