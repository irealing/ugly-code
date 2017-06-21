"""
命令行工具
"""
import inspect
import argparse


class Command(object):
    """
    Command object
    """

    def __init__(self, func):
        assert inspect.isfunction(func), "argument func must be function"
        params = inspect.signature(func).parameters
        self._keys = params.keys()
        self.func = func
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
            self.parser.add_argument(sar, default=pdf, required=is_require)

    @property
    def keys(self):
        """
        params list
        :return: 
        """
        return self._keys

    def __call__(self):
        """
        自动注入通过命令行获取的参数
        :return: 
        """
        _ns, _ = self.parser.parse_known_args()
        args = [getattr(_ns, key) for key in self._keys]
        return self.func(*args)
