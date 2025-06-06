import sys
from functools import lru_cache
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

    @lru_cache
    def get_logger(self):
        # 获取日志记录器实例，使用 lru_cache 缓存结果，避免重复创建
        return self.logger


# 创建 LogHelper 类的实例
LogHelpers = LogHelper()
# 获取日志记录器
log = LogHelpers.get_logger()
