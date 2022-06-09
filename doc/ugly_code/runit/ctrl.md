Module ugly_code.runit.ctrl
===========================

Classes
-------

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