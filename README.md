# ugly-code

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

使用[Type Hints](https://www.python.org/dev/peps/pep-0484/)的参数可自动进行类型检查.
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

* 即将更新

*[更多说明](https://fuser.cn/pythonzhuang-shi-qi-shi-jian-zhi-ming-ling-xing-gong-ju/)*
