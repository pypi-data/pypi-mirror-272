#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pkg-tool-lib',  # 包名
    version='0.1',  # 包的版本
    packages=find_packages(),  # 自动找到包中所有模块和子包
    author='Your Name',
    author_email='your.email@example.com',
    description='A small pkg tool demo package',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # README 文件为 markdown 格式
    url='https://github.com/yourusername/mypackage',  # 通常是代码托管的地址
    install_requires=[
        # 这里列出你包的依赖
        # 'requests',
    ],
    classifiers=[
        # 查看完整列表请访问 https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    # 可以添加更多setuptools选项
)
