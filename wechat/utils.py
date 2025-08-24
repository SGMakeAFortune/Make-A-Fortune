import logging
import operator

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
