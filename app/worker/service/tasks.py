import asyncio
from celery import Task, shared_task
from app.services.service import Service


class ServiceTask(Task):
    _m: Service = None

    @property
    def service(self):
        if self._m is None:
            self._m = Service()
        return self._m


@shared_task(base=ServiceTask, bind=True)
def work(self, q: str):
    return asyncio.run(self.service.work(q))
