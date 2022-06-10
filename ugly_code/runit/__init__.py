"""
`ugly_code.runit` 多任务管理工具。使用 `Runner`和`Worker`管理多进程程序。支持XML-RPC控制任务启停。

一个Worker对应一个进程，各进程使用tag区分。

使用方式:
    注册任务到Runner，启动Runner即可自动\手动启动任务或使用XML-RPC接口对任务进行调度管理。
"""
from .ctrl import RuntItMonitor
from .typing import RunIt, RunItException, Switch
from .worker import Runner, Worker

__all__ = ('RunIt', 'RunItException', 'Runner', 'Worker', 'RuntItMonitor', 'Switch')
__author__ = 'Memory_Leak<irealing@163.com>'
