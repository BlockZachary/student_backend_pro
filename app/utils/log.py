import logging
import sys
from functools import lru_cache
from types import FrameType
from typing import cast
from loguru import logger


class LogHelper:
    """
    实现日志系统
    """

    def __init__(self):
        # 初始化日志记录器
        self.logger = logger
        # 移除所有已有的日志处理器，清空日志设置
        self.logger.remove()
        # 定义日志输出的基本格式
        formatter = (
            "<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 绿色显示时间
            "{process.name} | "  # 显示进程名
            "{thread.name} | "  # 显示线程名
            "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 青色显示模块和方法名
            ":<cyan>{line}</cyan> | "  # 青色显示行号
            "<level>{level}</level>: "  # 显示日志级别
            "<level>{message}</level>",  # 显示日志内容
        )
        # 添加日志处理器，将日志输出到控制台
        # sys.stdout 表示标准输出，即控制台
        # 这里定义了详细的日志输出格式，包含时间、进程名、线程名、模块名、方法名、行号、日志等级和日志内容
        # 若需要自定义这些配置，可查看 loguru 官网的相关参数说明
        self.logger.add(
            sys.stdout,
            format=formatter[0],
        )

    def init_config(self):
        LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn", "fastapi", "app", "sqlalchemy.log",
                        "sqlalchemy.engine",
                        "sqlalchemy.engine.Engine")

        # 清空跟日志记录器的处理器
        logging.getLogger().handlers = [InterceptHandler()]

        # 为指定的日志记录器添加 LoguruHandler
        for logger_name in LOGGER_NAMES:
            logging_logger = logging.getLogger(logger_name)
            # 设置日志级别
            logging_logger.setLevel(logging.INFO)
            logging_logger.handlers = [InterceptHandler()]
            # 防止日志传播给根日志记录器，避免重复输出
            logging_logger.propagate = False

    @lru_cache
    def get_logger(self):
        # 获取日志记录器实例，使用 lru_cache 缓存结果，避免重复创建
        return self.logger

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # 将日志记录转换为 loguru 的日志格式
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # 获取当前调用栈的深度
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


# 创建 LogHelper 类的实例
LogHelpers = LogHelper()
# 获取日志记录器
log = LogHelpers.get_logger()
