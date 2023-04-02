from typing import Optional

from .listen import RabbitListenCtx, BaseListenCtx
from .define import ListenOpt, ConnectFunc, ConsumeFunc

__author__ = 'Memory_Leak<irealing@163.com>'
__all__ = ('RabbitListenCtx', 'ListenOpt', 'ConnectFunc', 'ConsumeFunc', 'default_listen_ctx')


def default_listen_ctx(opt: ListenOpt, conn: Optional[ConnectFunc] = None) -> 'RabbitListenCtx':
    return BaseListenCtx(opt, conn)
