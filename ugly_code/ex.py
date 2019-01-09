"""扩展工具模块"""
from typing import Any

__author__ = 'Memory_Leak<irealing@163.com>'
__all__ = ('ObjectProxy',)


class ObjectProxy(object):
    """
    对象代理工具
    """

    def __init__(self, obj: dict):
        self.__dict__['_raw'] = obj
        self.__dict__['_fields_cache'] = {}

    def __getattr__(self, item: str):
        if item in self._fields_cache:
            return self._fields_cache.get(item)
        if item not in self._raw:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, item))
        d = self._raw[item]
        if isinstance(d, dict):
            ret = self.__class__(d)
            self._fields_cache[item] = ret
        else:
            ret = self._raw[item]
        return ret

    def __setattr__(self, key: str, value: Any):
        raise PermissionError("attribute '{}' is readonly".format(key))

    def as_dict(self) -> dict:
        return self._raw
