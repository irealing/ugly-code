from typing import Sequence
from xmlrpc.client import ServerProxy

__author__ = 'Memory_Leak<irealing@163.com>'


class RuntItMonitor:
    def __init__(self, address: str):
        self.proxy = ServerProxy(address)

    def shutdown(self) -> int:
        return self.proxy.shutdown()

    def stats(self) -> Sequence[dict]:
        return self.proxy.stats()

    def close(self, tag: str, prefix: bool = False) -> int:
        return self.proxy.close(tag, prefix)

    def prune(self) -> int:
        return self.proxy.prune()

    def start(self, tag: int) -> int:
        return self.proxy.start(tag)
