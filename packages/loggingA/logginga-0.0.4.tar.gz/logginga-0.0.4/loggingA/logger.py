#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/12
# @Author  : alan
# @File    : logger.py

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from . import INFO, DEBUG

# 定义默认日志级别和日志文件后缀
DEFAULT_LOG_LEVEL = INFO
DEFAULT_LOG_SUFFIX = ".log"


def get_logger(project_path: str, log_name: str = "root", log_level: int = DEFAULT_LOG_LEVEL,
               log_suffix: str = DEFAULT_LOG_SUFFIX) -> logging.Logger:
    """
    获取日志对象
    :param project_path: 日志文件存放路径
    :param log_name: 日志名称，默认为"root"
    :param log_level: 日志级别，默认为INFO
    :param log_suffix: 日志文件后缀，默认为".log"
    :return: 日志对象
    """
    logger = logging.Logger(log_name)
    logger.setLevel(DEBUG)  # 这一步设置了整个 Logger 对象的日志级别。这个级别要低一些
    formatter = logging.Formatter(
        "%(asctime)s - %(process)d - %(thread)d - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s")

    # 定义日志文件路径
    log_file_path = os.path.join(project_path, '{}{}'.format(log_name, log_suffix))

    # 使用TimedRotatingFileHandler来处理日志文件滚动
    time_rotating_handler = TimedRotatingFileHandler(log_file_path,
                                                     when='d',
                                                     interval=1, backupCount=7,
                                                     encoding="utf8",
                                                     delay=False)
    time_rotating_handler.setLevel(log_level)
    time_rotating_handler.setFormatter(formatter)

    logger.addHandler(time_rotating_handler)

    return logger
