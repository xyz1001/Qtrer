#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='qtrer',
    version="1.0.3",
    description="对Qt翻译文件进行翻译的小工具",
    long_description="""根据翻译文档和OPENCC(简体和繁体转换)对Qt翻译文件进行翻译的小工具""",
    keywords='python Qt translate',
    author='xyz1001',
    author_email='zgzf1001@gmail.com',
    url='https://github.com/xyz1001/PythonToolkit/tree/master/toolkit/QTranslatorHelper',
    license='MIT',
    py_modules=['qtrer', 'excel_parser', 'opencc_translator', 'qt_ts'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['opencc-python-reimplemented',
                      'docopt', 'openpyxl', 'pandas'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    entry_points={'console_scripts': [
        'qtrer = qtrer:main',
    ]},
)
