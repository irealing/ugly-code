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
    """
    Switch，用于任务调度的开关对象
    """

    def __init__(self, name: str, retry: int = 0, delay: float = 1.0):
        """
        `Switch`的初始化函数

        :param name: 任务名称（即与之关联的任务标签）
        :param retry: `RunIt.serve` 指示执行结束或异常退出时是否需要重新开始,-1代表无限重试，0则不重试，大于0则为重试次数
        :param delay: 重试延迟时间
        """
        self._event = Event()
        self.name = name
        self.rc = retry
        self._delay = delay

    # 重试延迟时间
    delay = property(lambda self: max(self._delay, 1.0))

    @property
    def closed(self) -> bool:
        """已关闭"""
        return self._event.is_set()

    def close(self):
        """关闭开关"""
        _println("{} event set", self.name)
        return self._event.set()

    @property
    def on(self) -> bool:
        """已打开"""
        return not self._event.is_set()

    def retry_gen(self):
        c = 0
        while self.on and (self.rc < 0 or c <= self.rc):
            yield c
            time.sleep(self.delay)
            c += 1


class RunIt(metaclass=abc.ABCMeta):
    """
    RunIt

    抽象类，`ugly_code.runit` 的核心类。实现多进程服务种单一进程的调度管理。
    `Worker`和`Runner`的基类。
    """

    def __init__(self, switch: Switch):
        self._switch = switch

    @property
    def switch(self) -> Switch:
        """单一任务开关属性"""
        return self._switch

    @abc.abstractmethod
    def serve(self):
        """
        抽象方法，任务运行时执行的方法。
        """
        pass

    @property
    def tag(self) -> str:
        """单一任务唯一标签"""
        return self.switch.name

    def run(self):
        """启动任务时执行"""
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
        """
        输出消息到标准错误流

        :param message: 消息模板
        :param args: 参数
        """
        if args:
            message = message.format(*args)
        _println("{}:{}", self.tag, message)

    @abc.abstractmethod
    def shutdown(self):
        """
        关闭任务的回调方法

        收到退出任务的信号或其它原因关闭任务时执行
        """
        pass
