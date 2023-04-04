# ugly-code

[TOC]

## 安装

```shell
$ pip install ugly-code
```


## Command 工具

* 自动注入命令行参数到函数 (`ugly_code.cmd.Command`)


创建测试文件 `cmd_debug.py`

```python
from ugly_code.cmd import Command
    
@Command
def main(x:int, y ,z=1023):
    """
    测试一下
    """
    print("{x} \t {y} \t {z}".format(**locals()))

if __name__ == '__main__':
    globals()['main']()
```

执行该文件

```shell
$ python cmd_debug.py  -x 1023 -y 333
1023     333     1023
```

有默认值的参数会被设置为可选参数,无默认值则设置为必选.

使用[Type Hints](http://vvia.xyz/goyXNE)的参数可自动进行类型检查.
### 使用 CMDHolder持有 Command

* 创建命令行工具组

编辑文件`cmd_debug.py`

```python
from ugly_code.cmd import CMDHolder


@CMDHolder.command("test", "测试")
def main(x: int, b: str, c: int=1):
    """
    测试一下
    """
    print("{x} \t {y} \t {z}".format(**locals()))


@CMDHolder.command("echo", "echo")
def echo(words):
    """echo"""
    print(words)


if __name__ == '__main__':
    CMDHolder(__name__).execute()

```

执行该文件:

```shel
$ python3 cmd_debug.py echo -words "测试"
测试
$ python3 cmd_debug.py test
usage: Command line create by ugly-code.

    测试一下
     [-h] -x X -b B [-c C]
Command line create by ugly-code.

    测试一下
    : error: the following arguments are required: -x, -b
```

由示例可发现，CMDHolder可以持有多个命令行工具，根据不同的参数调用不同的命令行对象。而且还可以自定义命令行工具的名称与介绍。

## 多进程管理工具(ugly_code.runit)

`ugly_code.runit` 多任务管理工具。使用 `Runner`和`Worker`管理多进程程序。支持XML-RPC控制任务启停。

一个Worker对应一个进程，各进程使用tag区分。

使用方式:
    注册任务到Runner，启动Runner即可自动\手动启动任务或使用XML-RPC接口对任务进行调度管理。

### 示例

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

#### 使用xml-rpc管理进程

```python3
import threading
import time

from ugly_code.runit import Worker, Runner, RuntItMonitor


class AWorker(Worker):
    def serve(self):
        while self.switch.on:
            print(f"{self.switch.name} {time.time()}")
            time.sleep(3.0)


def start_and_close_task(m, tag):
    time.sleep(10)
    monitor = RuntItMonitor(m)
    monitor.start(tag)
    monitor.start(tag)
    time.sleep(3)
    print(monitor.stats())
    monitor.close(tag, True)
    time.sleep(3)
    monitor.prune()
    print(monitor.stats())
    monitor.shutdown()


if __name__ == '__main__':
    m = ('127.0.0.1', 65432)
    runner = Runner(None, (("a", AWorker, 0, 0, False), ('b', AWorker)), m=m)
    threading.Thread(target=start_and_close_task, args=("http://{}:{}".format(*m), "a",)).start()
    runner.run()

```

[查看文档](doc/ugly_code/runit/index.md)

## 扩展工具集

### 对象代理工具

```python
from ugly_code.ex import ObjectProxy

obj = ObjectProxy(dict(a=1, b=2, c=3, d=dict(a=1, b=2)))
print(obj.d.a)

```

## RabbitMQ监听工具

### 安装

```shell
$ pip install ugly-code[rabbit]
```

### 示例

```python

import threading
import time

from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from ugly_code.rabbit import ListenOpt, default_listen_ctx, RabbitListenCtx

opt = ListenOpt(
    queue='test',
    uri="amqp://guest:guest@127.0.0.1:5672/test",
    exchange='test',
    ext='direct',
    routing_key='test',
    durable=True,
    prefetch=1,
    retry_delay=1.0,
    retry=False
)


def handle_message(channel: BlockingChannel, deliver: Basic.Deliver, props: BasicProperties, body: bytes):
    print(body)
    channel.connection.process_data_events(3)


def close_it(val: RabbitListenCtx):
    time.sleep(10)
    val.shutdown()


with default_listen_ctx(opt).start(handle_message) as ctx:
    threading.Thread(target=close_it, args=(ctx,)).start()
```

*[更多说明](https://github.com/irealing/ugly-code)*