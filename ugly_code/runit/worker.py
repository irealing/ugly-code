import abc
import os
import threading
import time
from collections import defaultdict
from multiprocessing import Process, RLock
from typing import Callable, Tuple, Sequence, NamedTuple, Union
from xmlrpc.server import SimpleXMLRPCServer

from ._tool import _println
from .typing import RunIt, Switch, RunItException

__author__ = 'Memory_Leak<irealing@163.com>'


class Worker(RunIt, metaclass=abc.ABCMeta):
    """
    Worker抽象类，`ugly_code.runit` 的核心类。

    实现多进程服务种单一进程的调度管理。继承自`RunIt`。
    """

    def __init__(self, switch: Switch):
        super().__init__(switch)

    def shutdown(self):
        self.println("close worker {}", self.switch.name)
        self.switch.close()


class _ManagerItem(NamedTuple):
    tag: str
    seq: int
    process: Process
    switch: Switch


class WorkerManager:
    def __init__(self):
        self.lock = RLock()
        self._worker_mapping = {}
        self._counter = defaultdict(lambda: 0)

    def get_seq(self, tag: str) -> int:
        val = self._counter[tag]
        self._counter[tag] += 1
        return val

    def start(self, tag: str, f: Callable[[Switch], Worker], rc: int = 0, delay: float = 3.0):
        with self.lock:
            seq = self.get_seq(tag)
            switch = Switch(tag if not seq else "{}-{}".format(tag, seq), rc, delay)
            p = Process(target=f(switch), name=switch.name)
            self._worker_mapping[switch.name] = _ManagerItem(tag, seq, p, switch)
            p.start()
        return 1

    def prune(self):
        with self.lock:
            tags = filter(lambda it: not it.process.is_alive(), self._worker_mapping.values())
            c = 0
            for tag in tuple(tags):
                item = self._worker_mapping[tag.switch.name]
                item.process.close()
                del self._worker_mapping[tag.switch.name]
                c += 1
            return c

    def stats(self):
        with self.lock:
            return tuple(
                map(
                    lambda it: dict(tag=it.switch.name, alive=it.process.is_alive(), pid=it.process.pid),
                    self._worker_mapping.values()
                ))

    def close(self, tag: str, prefix: bool = False):
        with self.lock:
            if prefix:
                items = filter(lambda it: (it.switch.name.startswith(tag)), self._worker_mapping.values())
            else:
                items = (self._worker_mapping[tag],) if tag in self._worker_mapping else ()
            ret = 0
            for item in items:
                item.switch.close()
                ret += 1
            return ret

    def join(self):
        for item in self._worker_mapping.values():
            if not item.process.is_alive():
                continue
            _println("join {}", item.switch.name)
            item.process.join()


class _RegisterInfo(NamedTuple):
    tag: str
    f: Callable[[Switch], Worker]
    rc: int = 0
    rdelay: float = 3.0
    auto: bool = True


ManagerAddress = Union[Tuple[str, int], str]

WorkerInfo = Union[
    Tuple[str, Callable[[Switch], Worker]],
    Tuple[str, Callable[[Switch], Worker], int],
    Tuple[str, Callable[[Switch], Worker], int, float],
    Tuple[str, Callable[[Switch], Worker], int, float, bool],
]


class Runner(RunIt):
    """
    多进程任务调度工具

    :param switch: 控制Runner的开关，非必选
    :param fork: 注册多进程任务
    :param m: XML-RPC服务监听地址，为空则不启动XML-RPC服务

    fork 用户注册多进程任务,接手元组序列
    元组长度为2-5，五个参数分别为<br>
    | 任务名称 | 生成Worker对象的可执行对象 | 重试标志 | 重试延迟时间 | 是否自动启动(是否在Runner.run后启动) |

    示例
    ```python3
    import threading
    import time

    from ugly_code.runit import Switch, Worker, Runner


    class AWorker(Worker):
        def serve(self):
            while self.switch.on:
                print(f"{self.switch.name} {time.time()}")
                time.sleep(3.0)


    def close_it(switch: Switch):
        time.sleep(10)
        switch.close()


    if __name__ == '__main__':
        st = Switch('Runner')
        threading.Thread(target=close_it, args=(st,)).start()
        Runner(st, (("a", AWorker), ('b', AWorker)), m=('127.0.0.1', 0)).run()

    ```
    """

    def __init__(self, switch: Switch = None, fork: Sequence[WorkerInfo] = None, m: ManagerAddress = None):
        super().__init__(switch or Switch("{}:{}".format(self.__class__.__name__, os.getpid())))
        self._fork_mapping = {}
        if fork:
            self._fork_mapping.update(map(lambda p: (p[0], _RegisterInfo(*p)), fork))
        self._manager = WorkerManager()
        if m:
            m = (m, 0) if isinstance(m, str) else m
        self._m = m

    manager = property(lambda self: self._manager)

    def register(self, tag: str, f: Callable[[Switch], Worker], rc: int = 0, rdelay: float = 3.0, auto: bool = False):
        """
        注册任务

        :param tag: 任务标签
        :param f: 生成Worker对象的可执行对象
        :param rc: 重试标志
        :param rdelay: 重试延迟
        :param auto: 是否自动启动
        :return:
        """
        self._fork_mapping.update({tag: _RegisterInfo(tag, f, rc, rdelay, auto)})

    def start(self, tag: str):
        """使用tag启动新任务，已有相同tag任务则使用序号区分，即tag为"{tag}-{seq}"形式 """
        self.println("start process {}", tag)
        if tag not in self._fork_mapping:
            raise RunItException(404, 'unknown tag {}'.format(tag))
        info = self._fork_mapping[tag]
        self.manager.start(tag, info.f, info.rc, info.rdelay)
        return 1

    def serve(self):
        if self.switch.closed:
            return
        xml_server = self.make_rpc_worker()
        if xml_server:
            self.println("run xml rpc server on http://{}:{}", *xml_server.server_address)
        for info in self._fork_mapping.values():
            info.auto and self.start(info.tag)
        self.wait_for_close()
        xml_server and xml_server.server_close()
        self.manager.close("", True)
        self.manager.join()

    def wait_for_close(self):
        while self.switch.on:
            time.sleep(1.0)

    def shutdown(self):
        self.println("shutdown")
        self.switch.close()

    def stats(self):
        return self.manager.stats()

    def make_rpc_worker(self):
        if not self._m:
            return
        server = SimpleXMLRPCServer(self._m)
        server.register_instance(_RpcMonitor(self))
        threading.Thread(target=server.serve_forever, name="{}-XmlRpcServer".format(self.tag)).start()
        return server


class _RpcMonitor:
    def __init__(self, runner: Runner):
        self.runner = runner

    def stats(self):
        return self.runner.manager.stats()

    def close(self, tag: str, prefix: bool = False):
        return self.runner.manager.close(tag, prefix)

    def start(self, tag: str):
        return self.runner.start(tag)

    def prune(self):
        return self.runner.manager.prune()

    def shutdown(self):
        self.runner.shutdown()
        return 0
