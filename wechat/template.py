from datetime import datetime
from typing import Callable, Optional

from api.weather import ApiWeather
from models.header_models import HeaderDatabase
from models.weather_models import WeatherDataLoader
from wechat.utils import check_condition


def get_weather_message(weather_data: ApiWeather.Response) -> str:
    header = HeaderDatabase()
    header.load_from_file("../data/header.json")
    loader = WeatherDataLoader()
    loader.load_from_file("../data/weather.json")

    # 获取图标
    day_icon = loader.find_item_by_code(int(weather_data.iconDay))
    night_icon = loader.find_item_by_code(int(weather_data.iconNight))
    # pressure_icon = loader.find_item_by_code(int(weather_data.pressure))
    moon_icon = loader.find_item_by_code(int(weather_data.moonPhaseIcon))
    # 获取当前季节
    current_month = datetime.now().month
    season = loader.find_category_by_id(1012)
    season_icon = "?"
    season_name = "未知"
    for item in season.items:
        if int(current_month) in item.level:
            season_icon = item.choices
            season_name = item.name
    # 获取湿度
    humidity_icon = "💧"
    humidity_name = "适宜"
    humidity = loader.find_category_by_id(1015)
    for item in humidity.items:
        if check_condition(int(weather_data.humidity), item.condition):
            humidity_icon = item.choices
            humidity_name = item.name
    # 获取紫外线等级
    uv_index = loader.find_category_by_id(1011)
    uv_name = "正常"
    uv_icon = "🏠"
    for item in uv_index.items:
        if int(weather_data.uvIndex) in item.level:
            uv_icon = item.choices
            uv_name = item.name
    # 构建消息
    message = [
        f"{header.choice.to_str}\n",
        f"📅 日期: {weather_data.fxDate} | {season_name} {season_icon}",
        f"🌡️ 温度: {weather_data.tempMin}°C ~ {weather_data.tempMax}°C",
        f"☀️ 白天: {weather_data.textDay} {day_icon.choices}",
        f"🌙 夜间: {weather_data.textNight} {night_icon.choices if night_icon else ''}",
        f"🌬️ 白天风向: {weather_data.windDirDay} {weather_data.windScaleDay}级",
        f"🌌 夜间风向: {weather_data.windDirNight} {weather_data.windScaleNight}级",
        f"💧 湿度: {humidity_name} {humidity_icon} {weather_data.humidity}%",
        f"☂️ 紫外线: {uv_name} {uv_icon} 等级{weather_data.uvIndex}",
        f"🌧️ 降水: {weather_data.precip}mm",
        f"👀 能见度: {weather_data.vis}公里",
        f"☁️ 云量: {weather_data.cloud}%",
        f"📊 气压: {weather_data.pressure}hPa",
    ]

    # 添加日出日落信息（如果存在）
    if weather_data.sunrise and weather_data.sunset:
        message.append(f"🌅 日出: {weather_data.sunrise} | 日落: {weather_data.sunset}")

    # 添加月相信息（如果存在）
    if weather_data.moonPhase:
        moon_info = f"🌙 月相: {weather_data.moonPhase} {moon_icon.choices}"
        if weather_data.moonrise and weather_data.moonset:
            moon_info += (
                f" | 月出: {weather_data.moonrise} | 月落: {weather_data.moonset}"
            )
        message.append(moon_info)

    return "\n".join(message)


def template_concat(
    weather_message: str,
    suggestion_message: str,
    anniversary_message: str,
    calculation_message: str,
    reminder: Optional[Callable] = None,
    separator: str = "\n\n",
    max_length: Optional[int] = None,
) -> str:
    """
    拼接天气模板消息

    Args:
        weather_message: 天气信息
        suggestion_message: 建议信息
        anniversary_message: 纪念日信息
        calculation_message: 计算信息
        reminder: 提醒信息的回调函数
        separator: 各部分之间的分隔符
        max_length: 最大消息长度（可选）

    Returns:
        拼接后的完整消息
    """
    # 生成提醒信息
    reminder_message = reminder() if reminder else ""

    # 构建消息部分列表
    message_parts = []

    # 添加主要内容
    message_parts.extend(
        [
            weather_message,
            suggestion_message,
            anniversary_message,
            calculation_message,
            reminder_message,
        ]
    )

    # 拼接消息
    full_message = separator.join(message_parts)

    # 长度检查
    if max_length and len(full_message) > max_length:
        # 超长截断
        full_message = full_message[: max_length - 3] + "..."

    return full_message


def create_daily_reminder():
    """创建每日提醒"""
    now = datetime.now()
    return f"⏰ 每日提醒：今天是{now.month}月{now.day}日，记得保持好心情哦！"
