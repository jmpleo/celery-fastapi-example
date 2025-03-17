import json
import os
from typing import List, Any, Dict

import redis.asyncio as redis
from dotenv import load_dotenv
from celery import Signature, group, Celery
from pydantic import BaseModel

load_dotenv()


class TaskMeta(BaseModel):
    status: str


class GroupMeta(BaseModel):
    progress: int = 0
    tasks: List[str]


class TaskService:
    GROUP_KEY = 'task_service:group'
    TASK_KEY = 'task_service:task'

    def __init__(self, app: Celery):
        self.app = app

        self.redis_pool = redis.ConnectionPool.from_url(
            os.getenv('TASK_REDIS_URL'),
            encoding="utf-8",
            decode_responses=True,
        )
        self.redis_client = redis.Redis(connection_pool=self.redis_pool)

    async def start(self, task_sig: Signature) -> str:
        res = task_sig.apply_async()
        await self._update_task_meta(res.id, TaskMeta(status=res.status))
        return res.id

    async def start_group(self, tasks_sigs: List[Signature]) -> str:
        res = group(task_sig for task_sig in tasks_sigs).apply_async()
        res.save()
        await self._update_group_meta(
            res.id,
            GroupMeta(tasks=[r.id for r in res.results])
        )
        # Update each task meta with its current state
        for r in res.results:
            await self._update_task_meta(r.id, TaskMeta(status=r.state))
        return res.id

    async def get_task(
        self,
        task_id: str,
        include_result: bool = False,
    ) -> Any:
        exists = await self.redis_client.hexists(self.TASK_KEY, task_id)
        if exists:
            res = self.app.AsyncResult(id=task_id)
            meta = TaskMeta(status=res.state)
            await self._update_task_meta(task_id, meta)
            data = meta.model_dump()
            if include_result and res.state == "SUCCESS":
                data["result"] = res.result
            return data

    async def get_group(
        self, group_id: str,
        include_results: bool = False
    ) -> Any:
        exists = await self.redis_client.hexists(self.GROUP_KEY, group_id)
        if exists:
            res = self.app.GroupResult.restore(id=group_id)
            progress = 0
            results: Dict[str, Any] = {}
            for r in res.results:
                task_info = await self.get_task(
                    task_id=r.id,
                    include_result=include_results
                )
                if task_info and task_info['status'] == "SUCCESS":
                    progress += 1
                if include_results and task_info and 'result' in task_info:
                    results[r.id] = task_info['result']
            if include_results:
                return {"progress": progress, "results": results}
            return {"progress": progress}

    async def get_tasks(self) -> Any:
        tasks_info = await self.redis_client.hgetall(self.TASK_KEY)
        if tasks_info:
            tasks = {}
            for task_id in tasks_info:
                task_info = await self.get_task(task_id)
                if task_info:
                    tasks[task_id] = task_info
            return tasks

    async def get_groups(
        self,
        only_groups: bool = False
    ) -> Any:

        if only_groups:
            groups = await self.redis_client.hkeys(self.GROUP_KEY)
            return groups

        groups_info = await self.redis_client.hgetall(self.GROUP_KEY)
        if groups_info:
            tasks = await self.get_tasks()
            groups = {}
            for group_id, group_info in groups_info.items():
                group_parsed = json.loads(group_info)
                groups[group_id] = {
                    task_id: tasks[task_id]
                    for task_id in group_parsed.get('tasks', [])
                    if task_id in tasks
                }
            return groups

    async def _update_task_meta(self, task_id: str, meta: TaskMeta) -> None:
        await self.redis_client.hset(
            self.TASK_KEY,
            task_id,
            meta.model_dump_json()
        )

    async def _update_group_meta(self, group_id: str, meta: GroupMeta) -> None:
        await self.redis_client.hset(
            self.GROUP_KEY,
            group_id,
            meta.model_dump_json()
        )
