import abc
import logging
import time
from contextlib import contextmanager
from threading import Event
from typing import Optional, Tuple

from pika import BlockingConnection, URLParameters
from pika.adapters.blocking_connection import BlockingChannel

from ugly_code.rabbit.define import ListenOpt, ConnectFunc, ConsumeFunc

__author__ = 'Memory_Leak<irealing@163.com>'


class RabbitListenCtx(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, func: ConsumeFunc):
        pass

    @abc.abstractmethod
    def shutdown(self):
        pass

    @contextmanager
    def start(self, func: ConsumeFunc):
        yield self
        self.run(func)


class BaseListenCtx(RabbitListenCtx):
    def __init__(self, opt: ListenOpt, conn: Optional[ConnectFunc] = None):
        self._opt = opt
        self._conn = conn
        self._event = Event()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _connect(self) -> BlockingConnection:
        if self._conn:
            return self._conn()
        return BlockingConnection(URLParameters(self._opt.uri))

    def run(self, func: Optional[ConnectFunc]):
        while not self._event.is_set() and self._opt.retry:
            try:
                self._run_it(func)
            except Exception as e:
                self.logger.exception("run %s exception %s %s", self.__class__.__name__, e, e.__class__.__name__)
                if self._opt.retry_delay > 0:
                    time.sleep(self._opt.retry_delay)

    def _run_it(self, func: Optional[ConsumeFunc]):
        channel, tag = self._bind()
        msg_gen = channel.consume(self._opt.queue, False, inactivity_timeout=0.1)
        while not self._event.is_set():
            msg = next(msg_gen)
            if msg == (None, None, None):
                if self._event.is_set():
                    self.logger.info("close event is set,break")
                    break
                else:
                    continue
            method, properties, body = msg
            try:
                if func:
                    func(channel, method, properties, body)
                channel.basic_ack(method.delivery_tag)
            except Exception as e:
                self.logger.exception("invoce callback method exception %s %s", e.__class__.__name__, e)
                channel.basic_nack(method.delivery_tag)
        channel.cancel()
        channel.close()

    def _bind(self) -> Tuple[BlockingChannel, str]:
        connection = self._connect()
        channel = connection.channel()
        if self._opt.exchange:
            channel.exchange_declare(self._opt.exchange, self._opt.ext, durable=self._opt.durable)
        channel.queue_declare(self._opt.queue, durable=self._opt.durable, arguments=self._opt.arguments)
        if self._opt.exchange:
            routing_keys = (self._opt.routing_key,) if isinstance(self._opt.routing_key, str) else self._opt.routing_key
            for key in routing_keys:
                channel.queue_bind(self._opt.queue, self._opt.exchange, routing_key=key)
        return channel, channel.basic_qos(prefetch_count=self._opt.prefetch)

    def shutdown(self):
        self.logger.warning("shutdown now")
        self._event.set()
