import sys
from typing import Any

__author__ = 'Memory_Leak<irealing@163.com>'


def _println(message: str, *args: Any):
    if args:
        message = message.format(*args)
    sys.stderr.write("{}\n".format(message))
    sys.stderr.flush()
