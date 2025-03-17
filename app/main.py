import asyncio
from fastapi import (
    FastAPI, Body, Query, HTTPException,
    Depends, Request
)
from pydantic import BaseModel
from typing import List

from app.worker.worker import app as worker_app
from app.worker.service.tasks import work
from app.services.task import TaskService

app = FastAPI()
app.state.task_service = TaskService(app=worker_app)


def get_task_service(request: Request) -> TaskService:
    return request.app.state.task_service


@app.get("/start")
async def start(
    q: str = Query(...),
    task_service: TaskService = Depends(get_task_service)
):
    s = work.s(q=q)
    task_id = await task_service.start(s)
    return {"task_id": task_id}


@app.get("/task/{task_id}")
async def task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service)
):
    task_info = await task_service.get_task(
        task_id=task_id,
        include_result=True
    )
    if task_info:
        return task_info
    raise HTTPException(505)


@app.get("/group/{group_id}")
async def group(
    group_id: str,
    expand: int = Query(0),
    task_service: TaskService = Depends(get_task_service)
):
    group_info = await task_service.get_group(
        group_id=group_id,
        include_results=(expand != 0)
    )
    if group_info:
        return group_info
    raise HTTPException(505)


class PackStart(BaseModel):
    qs: List[str]


@app.post("/start")
async def bulk(
    request: PackStart = Body(...),
    task_service: TaskService = Depends(get_task_service)
):
    asyncio.create_task(
        task_service.start_group(
            tasks_sigs=[work.s(q) for q in request.qs]
        )
    )
    return {"status": "PENDING"}


@app.get("/tasks")
async def tasks(
    task_service: TaskService = Depends(get_task_service)
):
    tasks = await task_service.get_tasks()
    if tasks:
        return tasks
    raise HTTPException(500)


@app.get("/groups")
async def groups(
    task_service: TaskService = Depends(get_task_service)
):
    groups = await task_service.get_groups()
    if groups:
        return groups
    raise HTTPException(500)
