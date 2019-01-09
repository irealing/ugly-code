# ugly-code
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


## 安装方法

```shell
$ pip install ugly-code
```
## 网络/IP相关工具

### IP工具(IPv4)
#### IP地址和INT互转
```python
from ugly_code.net import IPv4
# IP地址转INT
iv = IPv4.ipn("192.168.99.0")
print(iv)
# 输出 3232260864
# INT 转为IP
ip=IPv4.nip(iv)
print(ip)
# 输出 192.168.99.0
```

#### 是否私有IP

```python
from ugly_code.net import IPv4

iv=IPv4("192.168.99.233")

print(iv.is_private())
# 输出 True
```

#### 其它

```python
from ugly_code.net import IPv4

ip = IPv4('192.168.99.233')
# 获取默认子网掩码
print(ip.default_mask_str())
# 输出  255.255.255.0

#  检测是否本地回环地址
print(ip.is_loop_back())
# 输出 False
```

* `IPv4`重写了包含 *>*、*<*、*==*、*!=*、*<=*、*>=* 的操作符

### Network工具

```python
from ugly_code.net import IPv4,Network

nt = Network('192.168.99.0',mask=24)
# 输出网络地址
print(nt.net_address())
# 输出 192.168.99.0
print(Network('10.0.0.235',mask=24))
# 输出 10.0.0.0
# 输出子网掩码
print(nt.mask())
# 输出 255.255.255.0
# 输出广播地址
print(nt.broadcast_address())
# 输出 192.168.99.255
# 检测 IP 是否在该网络中
print(IPv4('192.168.99.99') in nt)
# 输出结果 True
```
### 扩展工具集

#### 对象代理工具

```python
from ugly_code.ex import ObjectProxy

obj = ObjectProxy(dict(a=1, b=2, c=3, d=dict(a=1, b=2)))
print(obj.d.a)

```

*[更多说明](http://vvia.xyz/wnBAQb)*