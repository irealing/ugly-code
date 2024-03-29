import queue
import threading
import time
import unittest

from ugly_code.runit import Switch
from ugly_code.runit.extra import QueueInterface, MultiprocessQueueWorker


class TestQueue(QueueInterface[int]):

    def __init__(self):
        super().__init__()
        self.q = queue.Queue()

    def empty(self) -> bool:
        return self.q.empty()

    def pop(self, block: bool = True, timeout: float | None = None) -> int:
        return self.q.get(block, timeout)

    def put(self, t: int):
        return self.q.put(t)


def handle_sleep_time(sleep_time: float):
    time.sleep(sleep_time)


class TestMultiprocessQueueWorker(unittest.TestCase):
    def test_serve(self):
        on = Switch('test')
        q = TestQueue()
        threading.Thread(target=self.stop_it, args=(on,)).start()
        q.put(1)
        q.put(4)
        q.put(5)
        MultiprocessQueueWorker(on, q, handle_sleep_time, max_workers=1).serve()

    def stop_it(self, on: Switch, timeout: float = 10.0):
        time.sleep(timeout)
        on.close()
