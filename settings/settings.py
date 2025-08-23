import os

from settings.base import BaseConfig
from settings.development import DevelopmentSettings
from settings.production import ProductionSettings

# 环境映射关系
mapping = {
    "development": DevelopmentSettings,
    "production": ProductionSettings,
}


# 一键切换环境
APP_ENV = os.environ.get("APP_ENV", "development").lower()  # 设置环境变量为default
settings: BaseConfig = mapping[APP_ENV]()  # 获取指定的环境
