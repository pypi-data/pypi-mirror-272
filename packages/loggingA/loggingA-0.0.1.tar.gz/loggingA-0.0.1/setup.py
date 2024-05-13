#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/12
# @Author  : alan
# @File    : setup.py

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loggingA",  # 项目的名称，name是包的分发名称。独一无二
    version="0.0.1",  # 项目的版本。需要注意的是，PyPI上只允许一个版本存在，如果后续代码有了任何更改，再次上传需要增加版本号
    author="alan",  # 项目作者的名字和邮件, 用于识别包的作者。
    author_email="al6nlee@gmail.com",
    description="自定义日志模块",  # 项目的简短描述
    long_description=long_description,  # 项目的详细描述，会显示在PyPI的项目描述页面。必须是rst(reStructuredText) 格式的
    long_description_content_type="text/markdown",
    url="https://github.com/al6nlee/loggingA",
    packages=setuptools.find_packages(exclude=('tests', 'tests.*')),  # 指定最终发布的包中要包含的packages
    classifiers=[  # 其他信息，一般包括项目支持的Python版本，License，支持的操作系统
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development"
    ],
    install_requires=[],  # 项目依赖哪些库(内置库就可以不用写了)，这些库会在pip install的时候自动安装
    python_requires='>=3.8',
    license='MIT',
    package_data={  # 默认情况下只打包py文件，如果包含其它文件比如.so格式，增加以下配置
        "loggingA": [
            "*.py",
            "*.so",
        ]
    },
)
