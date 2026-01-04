"""统一的日志管理模块"""
import logging
import sys
from enum import Enum
from typing import Optional


class LogLevel(Enum):
    """日志级别"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""

    COLORS = {
        'DEBUG': '\033[36m',     # 青色
        'INFO': '\033[37m',      # 白色
        'WARNING': '\033[33m',   # 黄色
        'ERROR': '\033[31m',     # 红色
        'SUCCESS': '\033[32m',   # 绿色
        'RESET': '\033[0m'
    }

    ICONS = {
        'DEBUG': '🔍',
        'INFO': 'ℹ️',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'SUCCESS': '✅'
    }

    def format(self, record):
        """格式化日志记录"""
        level_name = record.levelname
        if level_name == 'CRITICAL':
            level_name = 'ERROR'

        color = self.COLORS.get(level_name, self.COLORS['RESET'])
        icon = self.ICONS.get(level_name, '')
        reset = self.COLORS['RESET']

        if hasattr(record, 'use_color') and record.use_color':
            # 带颜色的格式
            log_message = f"{color}{icon} [{level_name}]{reset} {record.getMessage()}"
        else:
            # 不带颜色的格式
            log_message = f"[{level_name}] {record.getMessage()}"

        return log_message


class MigrationLogger:
    """迁移工具日志管理器"""

    def __init__(self, name: str = "j2p_migration", verbose: bool = False,
                 use_color: bool = True):
        """
        初始化日志管理器

        Args:
            name: 日志器名称
            verbose: 是否显示详细日志 (包括 DEBUG 级别)
            use_color: 是否使用彩色输出
        """
        self.logger = logging.getLogger(name)
        self.verbose = verbose
        self.use_color = use_color

        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        self.logger.handlers.clear()

        import io
        if sys.platform == 'win32':
            if hasattr(sys.stdout, 'buffer'):
                stream = io.TextIOWrapper(
                    sys.stdout.buffer,
                    encoding='utf-8',
                    errors='replace',
                    line_buffering=True
                )
            else:
                stream = sys.stdout
        else:
            stream = sys.stdout

        console_handler = logging.StreamHandler(stream)
        console_handler.setLevel(logging.DEBUG)

        formatter = ColoredFormatter()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)

        logging.addLevelName(25, 'SUCCESS')

    def _log(self, level: str, message: str, **kwargs):
        """内部日志方法"""
        if level == 'SUCCESS':
        else:
            level_num = getattr(logging, level)

        extra = {'use_color': self.use_color}
        self.logger.log(level_num, message, extra=extra, **kwargs)

    def debug(self, message: str, **kwargs):
        """调试日志"""
        self._log('DEBUG', message, **kwargs)

    def info(self, message: str, **kwargs):
        """信息日志"""
        self._log('INFO', message, **kwargs)

    def warning(self, message: str, **kwargs):
        """警告日志"""
        self._log('WARNING', message, **kwargs)

    def error(self, message: str, **kwargs):
        """错误日志"""
        self._log('ERROR', message, **kwargs)

    def success(self, message: str, **kwargs):
        """成功日志"""
        self._log('SUCCESS', message, **kwargs)

    def section(self, title: str):
        """打印分节标题"""
        separator = "=" * 70
        self.info(f"\n{separator}")
        self.info(title)
        self.info(f"{separator}\n")

    def step(self, step_num: int, total_steps: int, description: str):
        """打印步骤信息"""
        self.info(f"步骤 {step_num}/{total_steps}: {description}")

    def progress(self, current: int, total: int, item: str = "项"):
        """打印进度信息"""
        percentage = (current / total * 100) if total > 0 else 0
        self.info(f"进度: {current}/{total} {item} ({percentage:.1f}%)")

    def exception(self, message: str, exc: Optional[Exception] = None):
        """记录异常"""
        if exc:
            self.error(f"{message}: {str(exc)}")
            if self.verbose:
                import traceback
                self.debug(traceback.format_exc())
        else:
            self.error(message)


_global_logger: Optional[MigrationLogger] = None


def get_logger(name: str = "j2p_migration", verbose: bool = False,
               use_color: bool = True) -> MigrationLogger:
    """获取全局日志实例"""
    global _global_logger
    if _global_logger is None:
        _global_logger = MigrationLogger(name, verbose, use_color)
    return _global_logger


def set_verbose(verbose: bool):
    """设置全局日志的详细程度"""
    global _global_logger
    if _global_logger:
        _global_logger.verbose = verbose
        if verbose:
            _global_logger.logger.setLevel(logging.DEBUG)
        else:
            _global_logger.logger.setLevel(logging.INFO)


# 便捷函数
def debug(message: str, **kwargs):
    """调试日志"""
    get_logger().debug(message, **kwargs)


def info(message: str, **kwargs):
    """信息日志"""
    get_logger().info(message, **kwargs)


def warning(message: str, **kwargs):
    """警告日志"""
    get_logger().warning(message, **kwargs)


def error(message: str, **kwargs):
    """错误日志"""
    get_logger().error(message, **kwargs)


def success(message: str, **kwargs):
    """成功日志"""
    get_logger().success(message, **kwargs)
