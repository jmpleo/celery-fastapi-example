import os
from typing import List, Any, Dict, Optional

import redis.asyncio as redis
from dotenv import load_dotenv
from celery import Signature, group, Celery
from pydantic import ValidationError
from loguru import logger

from app.schemas.task import TaskMeta, TaskResult, GroupMeta, GroupResult

load_dotenv()


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
        await self._update_task_meta(res.id, TaskMeta(ready=res.ready()))
        return res.id

    async def start_group(self, tasks_sigs: List[Signature]) -> str:
        res = group(task_sig for task_sig in tasks_sigs).apply_async()
        res.save()
        await self._update_group_meta(
            res.id,
            GroupMeta(
                ready=all(r.ready() for r in res.results),
                progress=sum(1 for r in res.results if r.ready())
            )
        )
        return res.id

    async def get_task(
        self,
        task_id: str,
        include_result: bool = False,
    ) -> Optional[TaskResult]:
        rec = await self._exec(self.redis_client.hget, self.TASK_KEY, task_id)
        if not rec:
            return None

        try:
            task_meta = TaskMeta.model_validate_json(rec)
        except ValidationError as e:
            logger.error(e)
            return None

        if task_meta.ready and not include_result:
            return TaskResult(**task_meta.model_dump())

        res = self.app.AsyncResult(id=task_id)
        if not res:
            return None

        task_meta.ready = res.ready()
        result = None
        if task_meta.ready and include_result:
            result = res.result

        await self._update_task_meta(task_id, task_meta)
        return TaskResult(result=result, **task_meta.model_dump())

    async def get_group(
        self, group_id: str,
        include_result: bool = False
    ) -> Optional[GroupResult]:
        rec = await self._exec(
            self.redis_client.hget, self.GROUP_KEY, group_id
        )
        if not rec:
            return None

        try:
            group_meta = GroupMeta.model_validate_json(rec)
        except ValidationError as e:
            logger.error(e)
            return None

        if group_meta.ready and not include_result:
            return GroupMeta(**group_meta.model_dump())

        res = self.app.GroupResult.restore(id=group_id)
        if not res:
            return None

        group_meta.ready = all(r.ready() for r in res.results)
        group_meta.progress = sum(1 for r in res.results if r.ready())

        results: Dict[str, Any] = {}
        if include_result:
            for r in res.results:
                if r.ready():
                    results[r.id] = r.result

        await self._update_group_meta(group_id, group_meta)
        return GroupResult(results=results, **group_meta.model_dump())

    async def get_tasks(self) -> Dict[str, TaskResult]:
        tasks = {}
        tasks_ids = await self._exec(
            self.redis_client.hkeys, self.TASK_KEY
        )
        if tasks_ids:
            for task_id in tasks_ids:
                task_result = await self.get_task(task_id)
                if task_result:
                    tasks[task_id] = task_result
        return tasks

    async def get_groups(self) -> Dict[str, GroupResult]:
        groups = {}
        groups_ids = await self._exec(self.redis_client.hkeys, self.GROUP_KEY)
        if groups_ids:
            for group_id in groups_ids:
                group_results = await self.get_group(group_id)
                if group_results:
                    groups[group_id] = group_results
        return groups

    async def _update_task_meta(self, task_id: str, meta: TaskMeta) -> None:
        await self._exec(
            self.redis_client.hset,
            self.TASK_KEY,
            task_id,
            meta.model_dump_json()
        )

    async def _update_group_meta(self, group_id: str, meta: GroupMeta) -> None:
        await self._exec(
            self.redis_client.hset,
            self.GROUP_KEY,
            group_id,
            meta.model_dump_json()
        )

    async def _exec(self, command, *args, **kwargs) -> Any:
        try:
            return await command(*args, **kwargs)
        except redis.ConnectionError as e:
            logger.warning(f"redis connection error: {e}")
        except Exception as e:
            logger.warning(f"redis execute command error: {e}")
