import logging
import operator

from concurrent_log_handler import ConcurrentRotatingFileHandler

logger = logging.getLogger(__name__)


def parse_condition(condition_str):
    """解析条件字符串，返回运算符和数值"""
    # 支持的所有运算符
    operators = [">=", "<=", "!=", "==", ">", "<"]

    for op in operators:
        if condition_str.startswith(op):
            try:
                value = float(condition_str[len(op) :])
                return op, value
            except ValueError:
                raise ValueError(f"无法解析数值: {condition_str[len(op):]}")

    raise ValueError(f"无效的条件格式: {condition_str}")


def check_condition(value, condition_str):
    """评估条件是否成立"""
    op, threshold = parse_condition(condition_str)

    operator_map = {
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
    }

    return operator_map[op](value, threshold)


def init_logger(
    logger_name,
    logger_level=logging.DEBUG,
    log_file: bool = False,
    multiprocess=False,
    console: bool = True,
    loggers: list = None,
    save_dir="logs",
):
    """初始化logger"""
    # 生成logger

    _logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - [%(pathname)s:%(lineno)d] - %(levelname)s: %(message)s"
    )
    if log_file:
        if multiprocess:
            file_handler = ConcurrentRotatingFileHandler(
                filename=f"{save_dir}/{logger_name}.log",
                mode="a",
                maxBytes=1024 * 1024 * 50,
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
    if console:
        # 终端流
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
    # 配置logger
    _logger.setLevel(logger_level)
    if log_file:
        _logger.addHandler(file_handler)
    if console:
        _logger.addHandler(console_handler)
    if loggers:
        for _logger_name in loggers:
            _logger = logging.getLogger(_logger_name)
            _logger.setLevel(logger_level)
            if log_file:
                _logger.addHandler(file_handler)
            if console:
                _logger.addHandler(console_handler)
    return _logger
