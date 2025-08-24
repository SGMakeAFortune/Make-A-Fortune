from settings.base import BaseConfig


class ProductionSettings(BaseConfig):
    """生产环境配置"""

    DEBUG = False

    LOGGER_LEVEL = "WARNING"

    HOUR = 7

    MINUTE = 30

    USER_NAME = "祖宗"
