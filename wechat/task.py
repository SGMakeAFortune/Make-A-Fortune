import logging
from datetime import datetime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from api.daily_sentence import ApiDailySentence
from api.weather import ApiWeather
from settings.settings import settings
from template import get_weather_message, template_concat
from wechat.date_calculation import AnniversaryMessageGenerator
from wechat.deepseek import get_suggestion

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/daily_message.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def send_daily_message():
    """发送每日消息的函数"""
    try:
        weather_api = ApiWeather()
        response = requests.request(
            weather_api.METHOD,
            weather_api.URL,
            headers=weather_api.Headers.load().to_dict,
            params=weather_api.Params.load().to_dict,
            timeout=weather_api.TIMEOUT,
        )
        daily = response.json().get("daily")[0]
        weather = weather_api.Response.load(daily)

        # 获取每日一句
        sentence_api = ApiDailySentence()
        response = requests.request(
            sentence_api.METHOD,
            sentence_api.URL,
            timeout=sentence_api.TIMEOUT,
        )
        sentence_response = sentence_api.Response.load(response.json())

        # 生成消息
        weather_message = get_weather_message(weather)
        suggestion_message = get_suggestion(weather_message)
        anniversary_message = AnniversaryMessageGenerator.generate_anniversary_message(
            datetime.strptime(settings.ANNIVERSARY, "%Y-%m-%d")
        )
        message = template_concat(
            weather_message,
            suggestion_message,
            anniversary_message,
            sentence_response.to_str,
        )
        from wxauto import WeChat  # 开源版

        # 发送微信消息
        wx = WeChat()
        wx.SendMsg(message, who="A-上官发财")

        logger.info(f"{datetime.now()} - 消息发送成功！")

    except Exception as e:
        logger.info(f"{datetime.now()} - 发送消息失败: {e}")


def setup_scheduler():
    """设置定时任务"""
    scheduler = BlockingScheduler()

    # 添加每天7点30执行的任务
    scheduler.add_job(
        send_daily_message,
        trigger=CronTrigger(hour=7, minute=30),
        id="daily_morning_message",
        name="每日早安消息",
        replace_existing=True,
    )

    return scheduler


if __name__ == "__main__":
    try:
        scheduler = setup_scheduler()
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("程序已退出")
    except Exception as e:
        logger.error(e, exc_info=True)
        logger.info(f"程序运行出错: {e}")
