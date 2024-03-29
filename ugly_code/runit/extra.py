import abc
import logging
import queue
import threading
import time
from concurrent.futures import ProcessPoolExecutor
from typing import Callable

from ugly_code.runit import Switch


class QueueInterface[T](metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def empty(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def pop(self, block: bool = True, timeout: float | None = None) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def put(self, t: T):
        raise NotImplementedError


class MultiprocessQueueWorker[T]:
    def __init__(
            self, on: Switch, tasks: QueueInterface[T], handler: Callable[[T], None], none_delay: float = 0.1,
            max_workers: int = 1
    ):
        self.on = on
        self.tasks = tasks
        self.handler = handler
        self.none_delay = none_delay
        self._max_workers = max_workers
        self.futures = queue.Queue()
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def max_workers(self) -> int:
        return self._max_workers

    @property
    def ready(self) -> bool:
        return self.max_workers > self.futures.qsize()

    def serve(self):
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            threading.Thread(target=self.watch_futures).start()
            while True:
                if not self.on.on:
                    executor.shutdown()
                    break
                if not self.ready:
                    self.sleep()
                    continue
                try:
                    if self.tasks.empty():
                        continue
                    task = self.tasks.pop(timeout=self.none_delay)
                    if not task:
                        self.sleep()
                except Exception as e:
                    self.logger.exception("Exception occurred while waiting for new task", exc_info=e)
                    self.sleep()
                    continue
                try:
                    self.logger.debug("receive new task")
                    f = executor.submit(self.handler, task)
                    self.futures.put(f)
                except Exception as e:
                    self.logger.exception("Exception occurred while submitting new task", exc_info=e)

    def sleep(self):
        time.sleep(self.none_delay)

    def watch_futures(self):
        while self.on.on or not self.futures.empty():
            try:
                if self.futures.empty():
                    self.sleep()
                    continue
                f = self.futures.get()
                if not f.done():
                    self.futures.put(f)
                f.result()
            except Exception as e:
                self.logger.exception("Exception occurred while watching futures %s %s", e.__class__.__name__, e)
