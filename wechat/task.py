import logging
from datetime import datetime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from api.daily_sentence import ApiDailySentence
from api.weather import ApiWeather
from settings.settings import settings
from wechat.date_calculation import AnniversaryMessageGenerator
from wechat.deepseek import get_suggestion
from .template import template_concat, WeatherMessageGenerator

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
        weather_message = WeatherMessageGenerator(
            "./data/header.json", "./data/weather.json"
        ).generate_random_style_message(weather)
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
        wx.SendMsg(message, who=settings.USER_NAME)

        logger.info(f"{datetime.now()} - 消息发送成功！")

    except Exception as e:
        logger.info(f"{datetime.now()} - 发送消息失败: {e}")


def setup_scheduler():
    """设置定时任务"""
    scheduler = BlockingScheduler()

    # 添加每天7点30执行的任务
    scheduler.add_job(
        send_daily_message,
        trigger=CronTrigger(hour=settings.HOUR, minute=settings.MINUTE),
        id="daily_morning_message",
        name="每日早安消息",
        replace_existing=True,
    )

    return scheduler


def run():
    try:
        logger.info("服务启动")
        logger.info("获取定时任务")
        scheduler = setup_scheduler()
        logger.info("定时任务启动")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("程序已退出")
    except Exception as e:
        logger.error(e, exc_info=True)
        logger.info(f"程序运行出错: {e}")
