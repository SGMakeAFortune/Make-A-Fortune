from settings.settings import settings
from wechat.task import run
from wechat.utils import init_logger

# 配置日志
logger = init_logger(
    settings.LOG_FILE_NAME,
    logger_level=settings.LOGGER_LEVEL,
    log_file=True,
    multiprocess=True,
    console=True,
    loggers=["wechat", "models"],
)


def main():
    run()


if __name__ == "__main__":
    main()
