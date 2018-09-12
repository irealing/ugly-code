"""
ugly-code 工具集
"""
from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 5):
    sys.exit("Sorry,Python < 3.5 is not supported !")
__author__ = "MemoryLeak"
setup(
    name="ugly_code",
    version="0.0.2",
    author=__author__,
    description="ugly-code tools",
    long_description=__doc__,
    packages=find_packages()
)
