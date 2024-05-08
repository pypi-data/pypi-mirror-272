# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pader',
    version='0.3',
    description='轻量级的爬虫框架，支持中间件、检验等功能',
    url='https://github.com/markadc/sqlman',
    author='WangTuo',
    author_email='markadc@126.com',
    packages=find_packages(),
    license='MIT',
    zip_safe=False,
    install_requires=['Requests', 'parsel', 'loguru', 'fake_useragent'],
    keywords=['Python', 'Spider'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
