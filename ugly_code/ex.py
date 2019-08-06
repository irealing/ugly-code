"""扩展工具模块"""
import json
from typing import Any

__author__ = 'Memory_Leak<irealing@163.com>'
__all__ = ('ObjectProxy', 'json_reader', 'load_json_config', 'text_writer')


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


def json_reader(filename: str):
    """
    从文件读取JSON数据
    :param filename:
    :return:
    """
    with open(filename, 'r', encoding='utf8') as input_stream:
        content = input_stream.read()
        return json.loads(content)


def load_json_config(env: dict, filename: str):
    """从JSON加载配置"""
    cfg = json_reader(filename)
    if not isinstance(cfg, dict):
        raise TypeError("json file {} is not dict".format(filename))
    for k, v in cfg.items():
        if k.startswith('_'):
            continue
        k = k.upper()
        if k in env:
            env[k] = v


def text_writer(filename: str, coding: str = 'utf-8'):
    """
    写入纯文本文档
    :param filename:
    :param coding:
    :return:
    """
    with open(filename, 'w', encoding=coding) as output:
        while True:
            line = yield
            if line is None:
                break
            output.write(line)
