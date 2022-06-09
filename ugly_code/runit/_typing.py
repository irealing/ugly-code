import abc
import os
import signal
import time
import traceback
from multiprocessing import Event
from typing import Any

from ._tool import _println

__author__ = 'Memory_Leak<irealing@163.com>'


class RunItException(Exception):

    def __init__(self, code: int, msg: str = '') -> None:
        super().__init__(code, msg)
        self._code = code
        self._msg = msg

    code = property(lambda self: self._code)
    msg = property(lambda self: self._msg)


class Switch:
    def __init__(self, name: str, retry: int = 0, delay: float = 1.0):
        self._event = Event()
        self.name = name
        self.rc = retry
        self._delay = delay

    delay = property(lambda self: self._delay)

    @property
    def closed(self) -> bool:
        return self._event.is_set()

    def close(self):
        _println("{} event set", self.name)
        return self._event.set()

    @property
    def on(self) -> bool:
        return not self._event.is_set()

    def retry_gen(self):
        c = 0
        while self.on and (self.rc < 0 or c <= self.rc):
            yield c
            time.sleep(self.delay)
            c += 1


class RunIt(metaclass=abc.ABCMeta):
    def __init__(self, switch: Switch):
        self._switch = switch

    switch = property(lambda self: self._switch)

    @abc.abstractmethod
    def serve(self):
        pass

    @property
    def tag(self) -> str:
        return self.switch.name

    def run(self):
        self._register_signal_exit()
        self.println("started pid={}", os.getpid())
        for _ in self.switch.retry_gen():
            try:
                self.serve()
                self.println("RunIt  complete")
            except Exception as e:
                self.println("catch exception {}", e)
                traceback.print_tb(e.__traceback__)

    def __call__(self):
        self.run()

    def _register_signal_exit(self):
        signal.signal(signal.SIGINT, self._on_sys_signal)
        signal.signal(signal.SIGTERM, self._on_sys_signal)

    def _on_sys_signal(self, sign, frame):
        self.println("receive sign {},call shutdown", sign)
        self.shutdown()

    def println(self, message: str, *args: Any):
        if args:
            message = message.format(*args)
        _println("{}:{}", self.tag, message)

    @abc.abstractmethod
    def shutdown(self):
        pass
