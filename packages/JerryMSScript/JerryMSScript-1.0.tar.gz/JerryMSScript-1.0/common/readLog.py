# -*- coding: utf-8 -*- 
"""
Author: JerryLaw
Time: 2023/11/15 8:32
Email: 623487850@qq.com
"""

import logging
import os
import time
from logging.handlers import RotatingFileHandler  # 按文件大小滚动备份

from common import setting
from common.setting import FilePath

log_path = FilePath.LOG
if not os.path.exists(log_path):
    print(log_path)
    os.mkdir(log_path)

logfile_name = os.path.join(log_path, "ApiTest{}.log".format(time.strftime("%Y%m%d")))


class RecordLog:
    def output_loggin(self):
        """get log object"""
        logger = logging.getLogger(__name__)
        # 防止重复打印重复的log日志
        if not logger.handlers:
            logger.setLevel(setting.LOG_LEVEL)
            # https://docs.python.org/zh-cn/3.9/library/logging.html#formatter-objects
            log_format = logging.Formatter(
                "%(levelname)s -%(asctime)s %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] -%(message)s")
            # 日志输出到指定位置
            # maxBytes:控制单个日志文件的大小(kb)，backupCount:用于控制文件文件的数量
            fh = RotatingFileHandler(filename=logfile_name,
                                     mode="a",
                                     maxBytes=5242880,
                                     backupCount=7,
                                     encoding="utf-8")
            fh.setLevel(setting.LOG_LEVEL)
            fh.setFormatter(log_format)

            # 将日志输出到控制台
            sh = logging.StreamHandler()
            sh.setLevel(setting.STREAM_LOG_LEVEL)
            sh.setFormatter(log_format)

            # 再将响应的handler(fh)和控制台输出handler(sh)添加到log对象
            logger.addHandler(fh)
            logger.addHandler(sh)

            return logger


apilog = RecordLog()
logs = apilog.output_loggin()
