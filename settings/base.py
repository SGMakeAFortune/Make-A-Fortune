import os

from dotenv import load_dotenv

load_dotenv()


def get_env_config(key: str):
    """从环境变量获取对应参数值

    Args:
        key (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    value = os.getenv(key)
    if not value:
        raise ValueError(f"未从环境变量中获取到{key}")
    return value


class BaseConfig:
    """基础配置文件

    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """

    DEBUG = True

    # get attribute
    def __getitem__(self, key):
        return self.__getattribute__(key)

    CREDENTIALS_ID = get_env_config("CREDENTIALS_ID")
    PROJECT_ID = get_env_config("PROJECT_ID")
    PRIVATE_KEY_PEM = get_env_config("PRIVATE_KEY_PEM")

    ANNIVERSARY = get_env_config("ANNIVERSARY")
    # 日志文件名
    TASK_FLASK_SERVER = "task-flask-server"
    # 日志级别
    LOGGER_LEVEL = "DEBUG"
    # DeepSeek API Key
    DEEPSEEK_API_KEY = get_env_config("DEEPSEEK_API_KEY")

    LOG_FILE_NAME = "daily_message.log"
