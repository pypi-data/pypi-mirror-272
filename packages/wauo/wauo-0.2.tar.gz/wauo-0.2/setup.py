# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='wauo',
    version='0.2',
    description='More convenient use of requests',
    url='https://github.com/markadc/wauo',
    author='WangTuo',
    author_email='markadc@126.com',
    packages=['wauo'],
    license='MIT',
    zip_safe=False,
    install_requires=['requests', 'fake_useragent', 'loguru'],
    keywords=['python', 'python3', 'requests', 'spider']
)
