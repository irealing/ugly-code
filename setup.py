"""
ugly-code 工具集
"""
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 5):
    sys.exit("Sorry,Python < 3.5 is not supported !")
__author__ = "MemoryLeak"
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
setup(
    name="ugly_code",
    url='http://vvia.xyz/wnBAQb',
    version="0.0.6",
    license='MIT',
    author=__author__,
    author_email='irealing@163.com',
    platforms='any',
    description="ugly-code tools",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages()
)
