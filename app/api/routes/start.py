from fastapi import APIRouter, Query, Body, Depends
from pydantic import BaseModel
from typing import List

from app.worker.service.tasks import work
from app.services.task import TaskService
from app.api.depends import get_task_service
from app.schemas.response import Response

r = APIRouter()


class PackStart(BaseModel):
    ns: List[int]


@r.get("", response_model=Response)
async def start(
    n: int = Query(...),
    task_service: TaskService = Depends(get_task_service)
) -> Response:
    task_id = await task_service.start(work.s(n))
    return Response(data={"task_id": task_id})


@r.post("", response_model=Response)
async def bulk(
    request: PackStart = Body(...),
    task_service: TaskService = Depends(get_task_service)
) -> Response:
    group_id = await task_service.start_group(work.s(n) for n in request.ns)
    return Response(data={"group_id": group_id})
