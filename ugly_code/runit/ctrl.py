from typing import Sequence
from xmlrpc.client import ServerProxy

__author__ = 'Memory_Leak<irealing@163.com>'


class RuntItMonitor:
    """使用XML-RPC管理调度`Runner`的客户端程序封装"""

    def __init__(self, address: str):
        self.proxy = ServerProxy(address)

    def shutdown(self) -> int:
        """关闭Runner"""
        return self.proxy.shutdown()

    def stats(self) -> Sequence[dict]:
        """查询进程信息"""
        return self.proxy.stats()

    def close(self, tag: str, prefix: bool = False) -> int:
        """使用tag关闭进程，使用相同tag启动的任务tag前缀相同，prefix为True则可关闭前缀相同的任务"""
        return self.proxy.close(tag, prefix)

    def prune(self) -> int:
        """清理已退出任务"""
        return self.proxy.prune()

    def start(self, tag: int) -> int:
        """使用tag启动新任务，已有相同tag任务则使用序号区分，即tag为"{tag}-{seq}"形式 """
        return self.proxy.start(tag)
