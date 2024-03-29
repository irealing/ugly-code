"""
ugly-code 工具集
"""

from setuptools import setup, find_packages

__author__ = "MemoryLeak"
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
setup(
    name="ugly_code",
    url='https://github.com/irealing/ugly-code',
    version="0.0.12", license='MIT',
    author=__author__,
    author_email='irealing@163.com',
    platforms='any',
    description="ugly-code tools",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.5",
    extras_require={
        "rabbit": ["pika"]
    }
)
