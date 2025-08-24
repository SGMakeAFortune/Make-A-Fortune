from datetime import datetime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from api.daily_sentence import ApiDailySentence
from api.weather import ApiWeather
from settings.settings import settings
from wechat.date_calculation import AnniversaryMessageGenerator
from wechat.deepseek import get_suggestion
from wechat.template import template_concat, WeatherMessageGenerator


def send_daily_message():
    """发送每日消息的函数"""

    try:
        # 获取天气信息
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
            "../data/header.json", "../data/weather.json"
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

        print(f"{datetime.now()} - 消息发送成功！")

    except Exception as e:
        print(f"{datetime.now()} - 发送消息失败: {e}")


def setup_scheduler():
    """设置定时任务"""
    scheduler = BlockingScheduler()

    # 测试任务
    scheduler.add_job(
        send_daily_message,
        trigger="date",
        run_date=datetime.now(),
        id="test_message",
        name="测试消息",
    )

    return scheduler


if __name__ == "__main__":
    print("开始启动每日消息定时任务...")
    print(f"将在每天自动发送消息给: A-上官发财")
    print(f"相识纪念日: {settings.ANNIVERSARY}")
    print("按 Ctrl+C 退出程序")

    try:
        scheduler = setup_scheduler()
        scheduler.start()
    except KeyboardInterrupt:
        print("程序已退出")
    except Exception as e:
        print(f"程序运行出错: {e}")
