#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/12
# @Author  : alan
# @File    : logger.py

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from . import INFO


def get_logger(project_path: str, log_name: str = "root") -> logging.Logger:
    logger = logging.Logger(log_name)
    logger.setLevel(INFO)  # 这一步设置了整个 Logger 对象的日志级别。这个级别要低一些
    formatter = logging.Formatter(
        "%(asctime)s - %(process)d - %(thread)d - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s")
    time_rotating_handler = TimedRotatingFileHandler(os.path.join(project_path, '{}.log'.format(log_name)),
                                                     when='d',
                                                     interval=1, backupCount=7,
                                                     encoding="utf8", delay=False)
    time_rotating_handler.setLevel(logging.INFO)  # 这一步设置了日志处理器（handler）的日志级别
    time_rotating_handler.setFormatter(formatter)
    logger.addHandler(time_rotating_handler)
    return logger
