from fastapi import APIRouter

from app.api.routes.start import r as r_start
from app.api.routes.group import r as r_group
from app.api.routes.task import r as r_task

r = APIRouter()

r.include_router(r_start, prefix='/start')
r.include_router(r_task, prefix='/task')
r.include_router(r_group, prefix='/group')
