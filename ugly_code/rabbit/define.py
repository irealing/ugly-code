from typing import NamedTuple, Union, Sequence, Optional, Callable, NoReturn

from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.exchange_type import ExchangeType
from pika.spec import Basic, BasicProperties

__author__ = 'Memory_Leak<irealing@163.com>'

ConsumeFunc = Callable[[BlockingChannel, Basic.Deliver, BasicProperties, bytes], NoReturn]
ConnectFunc = Callable[[], BlockingConnection]


class ListenOpt(NamedTuple):
    queue: str
    uri: str = ''
    exchange: str = ''
    ext: str = ExchangeType.fanout
    routing_key: Union[str, Sequence[str]] = ''
    durable: bool = True
    prefetch: int = 1
    arguments: Optional[dict] = None
    retry: bool = True
    retry_delay: float = 3.0
