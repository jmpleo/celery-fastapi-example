from pydantic import BaseModel
from typing import Any


class Response(BaseModel):
    error: str = ''
    data: Any = None
