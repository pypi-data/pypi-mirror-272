import asyncio
import logging
from typing import Any, Coroutine

from asynctaskpool.task_failed_exception import TaskFailedError


class TaskpoolTask:
    _logger = logging.getLogger(__name__)
    _no_result_yet = object()

    def __init__(self, task_id: object, future: Coroutine):
        self._event = asyncio.Event()
        self._task_id = task_id
        self._future = future
        self._result = self._no_result_yet
        self._failure: Exception | None = None

    async def wait_and_get_result(self) -> Any:
        self._logger.debug("Task %s in progress, waiting", self._task_id)
        await self._event.wait()

        if self._has_failed():
            self._logger.warning("Finished waiting for %s due to a failure", self._task_id)
            raise TaskFailedError("Task failed from another location") from self._failure
        else:
            self._logger.debug("Finished waiting for %s", self._task_id)
            return self._result

    async def run_task(self) -> Any:
        try:
            self._result = await self._future
            self._logger.debug("Task %s finished", self.task_id)
            return self._result
        except Exception as e:
            self._logger.error("Task %s failed", self.task_id)
            self._failure = e
            raise TaskFailedError() from e
        finally:
            self._mark_finished()

    def _mark_finished(self):
        self._event.set()

    @property
    def task_id(self):
        return self._task_id

    def _has_failed(self):
        return self._failure is not None
