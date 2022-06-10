Module ugly_code.runit.typing
=============================

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