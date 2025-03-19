from pydantic import BaseModel
from typing import Any, Dict


class TaskMeta(BaseModel):
    ready: bool


class TaskResult(TaskMeta):
    result: Any = None


class GroupMeta(TaskMeta):
    progress: int = 0


class GroupResult(GroupMeta):
    results: Dict[str, Any] = {}
