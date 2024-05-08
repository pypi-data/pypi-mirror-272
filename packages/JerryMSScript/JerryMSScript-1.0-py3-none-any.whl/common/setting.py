import logging
import os.path
import sys

# root directory
DIR_PATH = os.path.dirname(os.path.dirname(__file__))
# 添加到环境变量
sys.path.append(DIR_PATH)

LOG_LEVEL = logging.INFO  # 日志输出到文件的级别
STREAM_LOG_LEVEL = logging.INFO  # 输出日志到控制填


class FilePath:
    LOG = os.path.join(DIR_PATH, "log")