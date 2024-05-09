# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='wauo',
    version='0.5.1',
    description='爬虫者的贴心助手',
    url='https://github.com/markadc/wauo',
    author='WangTuo',
    author_email='markadc@126.com',
    packages=find_packages(),
    license='MIT',
    zip_safe=False,
    install_requires=['requests==2.28.1', 'fake_useragent==0.1.11', 'loguru==0.5.3'],
    keywords=['python', 'requests', 'spider'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
