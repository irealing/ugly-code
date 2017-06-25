#ugly-code

## 命令行工具

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