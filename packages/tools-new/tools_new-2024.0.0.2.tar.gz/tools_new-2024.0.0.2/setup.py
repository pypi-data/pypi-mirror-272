#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @time     : 2024/5/9 17:47
# @Author   : new
# @File      : setup.py
from setuptools import setup, find_packages

GFICLEE_VERSION = '2024.0.0.2'

setup(
    name='tools_new',
    version=GFICLEE_VERSION,
    packages=find_packages(),
    include_package_data=True,
    entry_points={

        "console_scripts": ['tools_new = tools_py.main:main']
    },
    install_requires=['portion', 'python-dateutil', 'paramiko', 'redis', 'jsonpath', 'pymysql',
                      'apscheduler', 'requests', 'xlrd', 'pymongo', 'SQLAlchemy'],
    url='http://git.ppdaicorp.com/pengying/tools_py.git',
    license='MIT',
    author='py_new',
    author_email='pengying@ppdai.com',
    description='More convenient to create tools project'
)