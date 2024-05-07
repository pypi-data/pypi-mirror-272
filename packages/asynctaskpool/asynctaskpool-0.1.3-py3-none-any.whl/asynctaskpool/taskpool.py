import asyncio
import logging
from typing import TypeVar, Generic, Any, Coroutine

from .task_failed_exception import TaskFailedError
from .taskpool_task import TaskpoolTask

T = TypeVar("T")


class AsyncTaskPool(Generic[T]):
    """
    A TaskPool is a utility that receives submitted tasks which have an identity and which should be executed no more
    than once, even in parallel.
    """

    _logger = logging.getLogger(__name__)

    def __init__(self, restart_if_finished: bool = False):
        self._task_tracker: dict[object, asyncio.Event | T | None] = {}
        self._semaphore = asyncio.Semaphore()
        self._restart_task_if_finished: bool = restart_if_finished

    def take_in_precomputed_result_map(self, results: dict[object, T]) -> None:
        self._task_tracker.update(**results)

    async def wait_for_task_to_finish_if_running(self, task_id: object) -> bool:
        async with self._semaphore:
            if self._has_task_been_submitted_yet(task_id):
                task_to_wait_for = self._get_tracked_task(task_id)

                if self._has_task_finished(task_to_wait_for):
                    self._logger.debug("Task %s has already finished, do not need to wait", task_id)
                    return False
            else:
                self._logger.debug("Task %s has not been started", task_id)
                return False

        self._logger.debug("Waiting for task %s", task_id)

        # Ignore result, we don't need it
        await task_to_wait_for.wait_and_get_result()
        return True

    async def submit_new_task(self, task_id: object, future: Coroutine) -> T | None:
        # Any async item that we need to await is put into this.
        # Then we await it at the end of the function, so we can use exception-safe 'with' block without holding the semaphore too long.
        async_operation_to_wait_for: Coroutine | None = None

        async with self._semaphore:
            if self._has_task_been_submitted_yet(task_id):
                task = self._get_tracked_task(task_id)

                if self._has_task_finished(task):
                    if not self._restart_task_if_finished:
                        self._logger.debug("Task %s already finished, returning.", task_id)
                        return task
                    else:
                        async_operation_to_wait_for = self._create_and_run_task(task_id, future)
                else:
                    async_operation_to_wait_for = task.wait_and_get_result()
            else:
                async_operation_to_wait_for = self._create_and_run_task(task_id, future)

        if async_operation_to_wait_for is not None:
            return await async_operation_to_wait_for

    def _has_task_been_submitted_yet(self, task_id: object):
        return task_id in self._task_tracker.keys()

    def _get_tracked_task(self, task_id: object) -> TaskpoolTask | T | None:
        return self._task_tracker[task_id]

    def _create_and_track_new_unstarted_task(self, task_id: object, future: Coroutine) -> TaskpoolTask:
        self._logger.debug("Creating new task %s.", task_id)
        new_in_progress_task = TaskpoolTask(task_id=task_id, future=future)
        self._track_new_task(new_in_progress_task)
        return new_in_progress_task

    def _track_new_task(self, task: TaskpoolTask):
        self._task_tracker[task.task_id] = task

    async def _record_result_of_task(self, task: TaskpoolTask, result: Any):
        async with self._semaphore:
            self._task_tracker[task.task_id] = result

    async def _create_and_run_task(self, task_id: object, future: Coroutine):
        new_task = self._create_and_track_new_unstarted_task(task_id=task_id, future=future)
        return await self._run_task_and_record_result(new_task)

    async def _run_task_and_record_result(self, task: TaskpoolTask) -> T:
        try:
            task_result = await task.run_task()
            await self._record_result_of_task(task=task, result=task_result)
            return task_result
        except TaskFailedError as e:
            self._erase_task_due_to_failure(task)
            raise e

    def _erase_task_due_to_failure(self, task: TaskpoolTask):
        self._logger.warning("Removing tracking for task %s due to it failing", task.task_id)
        del self._task_tracker[task.task_id]

    def clear_results(self) -> None:
        self._task_tracker.clear()

    def get_results_of_all_completed_tasks(self) -> list[T]:
        def exclude_none_and_unfinished_tasks(it):
            return it is not None and self._has_task_finished(it)

        return list(filter(exclude_none_and_unfinished_tasks, self._task_tracker.values()))

    @staticmethod
    def _has_task_finished(task: Any) -> bool:
        return not isinstance(task, TaskpoolTask)
