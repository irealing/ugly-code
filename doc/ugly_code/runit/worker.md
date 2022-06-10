Module ugly_code.runit.worker
=============================

Classes
-------

`Runner(switch: ugly_code.runit.typing.Switch = None, fork: Sequence[Union[Tuple[str, Callable[[ugly_code.runit.Switch], ugly_code.runit.worker.Worker]], Tuple[str, Callable[[ugly_code.runit.Switch], ugly_code.runit.worker.Worker], int], Tuple[str, Callable[[ugly_code.runit.Switch], ugly_code.runit.worker.Worker], int, float], Tuple[str, Callable[[ugly_code.runit.Switch], ugly_code.runit.worker.Worker], int, float, bool]]] = None, m: Union[Tuple[str, int], str] = None)`
:   多进程任务调度工具
    
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

    ### Ancestors (in MRO)

    * ugly_code.runit.typing.RunIt

    ### Instance variables

    `manager`
    :

    ### Methods

    `make_rpc_worker(self)`
    :

    `register(self, tag: str, f: Callable[[ugly_code.runit.Switch], ugly_code.runit.worker.Worker], rc: int = 0, rdelay: float = 3.0, auto: bool = False)`
    :   注册任务
        
        :param tag: 任务标签
        :param f: 生成Worker对象的可执行对象
        :param rc: 重试标志
        :param rdelay: 重试延迟
        :param auto: 是否自动启动
        :return:

    `start(self, tag: str)`
    :   使用tag启动新任务，已有相同tag任务则使用序号区分，即tag为"{tag}-{seq}"形式

    `stats(self)`
    :

    `wait_for_close(self)`
    :

`Worker(switch: ugly_code.runit.typing.Switch)`
:   Worker抽象类，`ugly_code.runit` 的核心类。
    
    实现多进程服务种单一进程的调度管理。继承自`RunIt`。

    ### Ancestors (in MRO)

    * ugly_code.runit.typing.RunIt

`WorkerManager()`
:   

    ### Methods

    `close(self, tag: str, prefix: bool = False)`
    :

    `get_seq(self, tag: str) ‑> int`
    :

    `join(self)`
    :

    `prune(self)`
    :

    `start(self, tag: str, f: Callable[[ugly_code.runit.Switch], ugly_code.runit.worker.Worker], rc: int = 0, delay: float = 3.0)`
    :

    `stats(self)`
    :