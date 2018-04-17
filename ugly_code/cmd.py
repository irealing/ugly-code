"""
命令行工具
"""
import argparse
import inspect
import sys
from types import FunctionType


class Command(object):
    """
    Command object
    """

    def __init__(self, func: FunctionType):
        assert inspect.isfunction(func), "argument func must be function"
        params = inspect.signature(func).parameters
        self._keys = params.keys()
        self.func = func
        self._name = func.__name__
        self._describe = func.__doc__
        usage = "Command line create by ugly-code.\n{}".format(func.__doc__)
        self.parser = argparse.ArgumentParser(usage)
        for key in self.keys:
            param = params[key]
            pt = param.annotation
            if pt is inspect._empty:
                pt = None
            sar = '-{}'.format(key)
            is_require = param.default is inspect._empty
            pdf = None if is_require else param.default
            self.parser.add_argument(
                sar, type=pt, default=pdf, required=is_require)

    @property
    def name(self):
        """
        名称
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        设置名称
        """
        self._name = value

    @property
    def describe(self):
        """说明"""
        return self._describe

    @describe.setter
    def describe(self, value):
        """
        设置说明
        """
        self._describe = value

    @property
    def keys(self):
        """
        params list
        :return: str
        """
        return self._keys

    def __call__(self):
        """
        自动注入通过命令行获取的参数
        :return: str
        """
        _ns, _ = self.parser.parse_known_args()
        args = [getattr(_ns, key) for key in self._keys]
        return self.func(*args)


class CMDHolder(object):
    """
    持有command对象
    """

    def __init__(self, import_name: str = '__main__'):
        """
        初始化
        :param import_name: 导入Command 的 module
        """
        assert import_name in sys.modules, 'module not found {}'.format(
            import_name)
        scope = sys.modules[import_name].__dict__
        self._operation = {
            item.name: item for item in scope.values() if isinstance(item, Command)}
        self._usage = None

    @property
    def usage(self):
        """
        描述信息
        :return: str
        """
        if not self._usage:
            detail = "\n".join(('\t{}\t{}'.format(item.name, item.describe)
                                for item in self._operation.values()))
            self._usage = 'Create by {}\n{}'.format(CMDHolder.__name__, detail)
        return self._usage

    @staticmethod
    def command(name: str, describe: str = "")->Command:
        """
        创建Command对象
        """
        def _wrap(func):
            cmd = Command(func)
            cmd.name = name
            if describe:
                cmd.describe = describe
            return cmd
        return _wrap

    def execute(self):
        """
        执行操作
        :return: 
        """
        operation = sys.argv[1] if len(sys.argv) > 1 else None
        if not operation or operation not in self._operation:
            print(self.usage)
            sys.exit('Unsupported Operation {}.'.format(operation))
        self._operation[operation]()
