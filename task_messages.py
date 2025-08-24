import logging

from settings.settings import settings
from wechat.task import setup_scheduler

# 配置日志
logging.basicConfig(
    level=settings.LOGGER_LEVEL,
    format="%(asctime)s - [%(pathname)s:%(lineno)d] - %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(f"./logs/{settings.LOG_FILE_NAME}", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def main():
    try:
        scheduler = setup_scheduler()
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("程序已退出")
    except Exception as e:
        logger.error(e, exc_info=True)
        logger.info(f"程序运行出错: {e}")


if __name__ == "__main__":
    main()
