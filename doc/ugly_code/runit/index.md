Module ugly_code.runit
======================
`ugly_code.runit` 多任务管理工具。使用 `Runner`和`Worker`管理多进程程序。支持XML-RPC控制任务启停。

一个Worker对应一个进程，各进程使用tag区分。

使用方式:
    注册任务到Runner，启动Runner即可自动\手动启动任务或使用XML-RPC接口对任务进行调度管理。


Classes
-------

`RunIt(switch: ugly_code.runit.typing.Switch)`
:   RunIt
    
    抽象类，`ugly_code.runit` 的核心类。实现多进程服务种单一进程的调度管理。
    `Worker`和`Runner`的基类。

    ### Descendants

    * ugly_code.runit.worker.Runner
    * ugly_code.runit.worker.Worker

    ### Instance variables

    `switch: ugly_code.runit.typing.Switch`
    :   单一任务开关属性

    `tag: str`
    :   单一任务唯一标签

    ### Methods

    `println(self, message: str, *args: Any)`
    :   输出消息到标准错误流
        
        :param message: 消息模板
        :param args: 参数

    `run(self)`
    :   启动任务时执行

    `serve(self)`
    :   抽象方法，任务运行时执行的方法。

    `shutdown(self)`
    :   关闭任务的回调方法
        
        收到退出任务的信号或其它原因关闭任务时执行

`RunItException(code: int, msg: str = '')`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

    ### Instance variables

    `code`
    :

    `msg`
    :

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

`RuntItMonitor(address: str)`
:   使用XML-RPC管理调度`Runner`的客户端程序封装

    ### Methods

    `close(self, tag: str, prefix: bool = False) ‑> int`
    :   使用tag关闭进程，使用相同tag启动的任务tag前缀相同，prefix为True则可关闭前缀相同的任务

    `prune(self) ‑> int`
    :   清理已退出任务

    `shutdown(self) ‑> int`
    :   关闭Runner

    `start(self, tag: int) ‑> int`
    :   使用tag启动新任务，已有相同tag任务则使用序号区分，即tag为"{tag}-{seq}"形式

    `stats(self) ‑> Sequence[dict]`
    :   查询进程信息

`Switch(name: str, retry: int = 0, delay: float = 1.0)`
:   Switch，用于任务调度的开关对象
    
    `Switch`的初始化函数
    
    :param name: 任务名称（即与之关联的任务标签）
    :param retry: `RunIt.serve` 指示执行结束或异常退出时是否需要重新开始,-1代表无限重试，0则不重试，大于0则为重试次数
    :param delay: 重试延迟时间

    ### Instance variables

    `closed: bool`
    :   已关闭

    `delay`
    :

    `on: bool`
    :   已打开

    ### Methods

    `close(self)`
    :   关闭开关

    `retry_gen(self)`
    :

`Worker(switch: ugly_code.runit.typing.Switch)`
:   Worker抽象类，`ugly_code.runit` 的核心类。
    
    实现多进程服务种单一进程的调度管理。继承自`RunIt`。

    ### Ancestors (in MRO)

    * ugly_code.runit.typing.RunIt