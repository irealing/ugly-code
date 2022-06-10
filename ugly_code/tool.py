import importlib
import sys
from typing import Sequence, Generator, Any

__all__ = ('load_variables', "load_variable")

__author__ = 'Memory_Leak<irealing@163.com>'


def load_variables(paths: Sequence[str], package: str = __package__) -> Generator[Any, None, None]:
    yield from map(lambda pn: load_variable(pn, package), paths)


def load_variable(pn: str, package) -> Any:
    mn, var = pn.split(":")
    sys.stderr.write("import module {} {}\n".format(mn, package))
    module = importlib.import_module(mn, package=package)
    return getattr(module, var, None)
