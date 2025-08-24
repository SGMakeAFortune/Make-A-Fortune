from settings.base import BaseConfig


class DevelopmentSettings(BaseConfig):
    """开发环境配置"""

    DEBUG = True

    HOUR = 7

    MINUTE = 30

    USER_NAME = "上官发财"
