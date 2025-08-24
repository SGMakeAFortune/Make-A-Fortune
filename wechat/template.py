import logging
import random
from datetime import datetime
from typing import Any, Callable, Optional

from models.header_models import HeaderDatabase
from models.weather_models import WeatherDataLoader
from wechat.utils import check_condition

logger = logging.getLogger(__name__)


class WeatherMessageGenerator:
    def __init__(self, header_path: str, weather_data_path: str):
        self.header = HeaderDatabase()
        self.header.load_from_file(header_path)
        self.loader = WeatherDataLoader()
        self.loader.load_from_file(weather_data_path)

        # 消息模板库
        self.templates = {
            "romantic": [
                "🌙✨ {date} | 在{season}的怀抱里 {season_icon}",
                "🌡️ 温度: {temp_min}°C ~ {temp_max}°C | 爱你的温度刚刚好 ❤️",
                "☀️ 白天: {day_icon} {day_name} | 像你的笑容一样温暖 {day_icon}",
                "🌙 夜间: {night_icon} {night_name} | 月光如你的眼眸般温柔 {night_icon}",
                "💧 湿度: {humidity_name} {humidity_icon} {humidity}% | 空气里弥漫着甜蜜的气息",
                "☂️ 紫外线: {uv_name} {uv_icon} | 我们的爱情需要防晒吗？等级 {uv_index}",
                "🌧️ 降水: {precip}mm | 如果是雨，那也是浪漫的太阳雨",
                "👀 能见度: {vis_name} {vis_icon} {vis}公里 | 我能看见我们的未来",
                "🌅 日出: {sunrise} | 日落: {sunset} | 想你的时间从日出到日落",
                "🌙 月相: {moon_name} {moon_icon} | 月出: {moonrise} | 月落: {moonset}",
            ],
            "cute": [
                "🐰🌈 {date} | {season}小精灵来啦 {season_icon}",
                "🌡️ 温度: {temp_min}°C ~ {temp_max}°C | 暖暖的像小熊的拥抱 🧸",
                "☀️ 白天: {day_icon} {day_name} | 太阳公公在微笑哦 {day_icon}",
                "🌙 夜间: {night_icon} {night_name} | 月亮婆婆讲故事时间 {night_icon}",
                "💧 湿度: {humidity_name} {humidity_icon} {humidity}% | 空气湿润润的像果冻",
                "☂️ 紫外线: {uv_name} {uv_icon} | 小兔子要涂防晒霜啦！等级 {uv_index}",
                "🌧️ 降水: {precip}mm | 雨滴在跳圆舞曲呢",
                "👀 能见度: {vis_name} {vis_icon} {vis}公里 | 能看到好多棉花糖云朵",
                "🌅 日出: {sunrise} | 日落: {sunset} | 太阳宝宝起床睡觉时间",
                "🌙 月相: {moon_name} {moon_icon} | 月出: {moonrise} | 月落: {moonset}",
            ],
            "playful": [
                "🎪🤹 {date} | {season}马戏团开演啦 {season_icon}",
                "🌡️ 温度: {temp_min}°C ~ {temp_max}°C | 热到可以煎鸡蛋了！ 🍳",
                "☀️ 白天: {day_icon} {day_name} | 太阳在开个人演唱会 {day_icon}",
                "🌙 夜间: {night_icon} {night_name} | 月亮在玩捉迷藏 {night_icon}",
                "💧 湿度: {humidity_name} {humidity_icon} {humidity}% | 空气湿得像刚洗完澡",
                "☂️ 紫外线: {uv_name} {uv_icon} | 防晒霜，启动！等级 {uv_index}",
                "🌧️ 降水: {precip}mm | 雨神今天比较节俭",
                "👀 能见度: {vis_name} {vis_icon} {vis}公里 | 能看到邻居家的猫在干嘛",
                "🌅 日出: {sunrise} | 日落: {sunset} | 太阳的上下班时间",
                "🌙 月相: {moon_name} {moon_icon} | 月出: {moonrise} | 月落: {moonset}",
            ],
            "poetic": [
                "📜🌸 {date} | {season}的诗篇正在书写 {season_icon}",
                "🌡️ 温度: {temp_min}°C ~ {temp_max}°C | 恰似温柔的拥抱",
                "☀️ 白天: {day_icon} {day_name} | 光与影的完美和声 {day_icon}",
                "🌙 夜间: {night_icon} {night_name} | 星空下的静谧独白 {night_icon}",
                "💧 湿度: {humidity_name} {humidity_icon} {humidity}% | 空气中弥漫着诗意的露珠",
                "☂️ 紫外线: {uv_name} {uv_icon} | 阳光的诗行，等级 {uv_index}",
                "🌧️ 降水: {precip}mm | 天空的泪滴，大地的甘霖",
                "👀 能见度: {vis_name} {vis_icon} {vis}公里 | 远方的山峦若隐若现",
                "🌅 日出: {sunrise} | 日落: {sunset} | 昼夜交替的华美乐章",
                "🌙 月相: {moon_name} {moon_icon} | 月出: {moonrise} | 月落: {moonset}",
            ],
            "tech": [
                "🤖📊 {date} | {season}数据报告 {season_icon}",
                "🌡️ 温度: {temp_min}°C ~ {temp_max}°C | 热力学参数正常",
                "☀️ 白天: {day_icon} {day_name} | 太阳辐射强度: 标准 {day_icon}",
                "🌙 夜间: {night_icon} {night_name} | 月光反射率: 正常 {night_icon}",
                "💧 湿度: {humidity_name} {humidity_icon} {humidity}% | 水分子浓度: 偏高",
                "☂️ 紫外线: {uv_name} {uv_icon} | 电磁波谱分析，等级 {uv_index}",
                "🌧️ 降水: {precip}mm | 液态水沉淀量",
                "👀 能见度: {vis_name} {vis_icon} {vis}公里 | 光学透明度: 优秀",
                "🌅 日出: {sunrise} | 日落: {sunset} | 地球自转时间标记",
                "🌙 月相: {moon_name} {moon_icon} | 月出: {moonrise} | 月落: {moonset}",
            ],
        }

    def _get_season_info(self) -> tuple:
        """获取季节信息"""
        current_month = datetime.now().month
        season = self.loader.find_category_by_id(1012)
        season_icon = "❓"
        season_name = "未知季节"

        for item in season.items:
            if current_month in item.level:
                season_icon = item.get_icon
                season_name = item.get_name
                break

        return season_name, season_icon

    def _get_humidity_info(self, humidity_value: int) -> tuple:
        """获取湿度信息"""
        humidity = self.loader.find_category_by_id(1015)
        humidity_icon = "💧"
        humidity_name = "适宜"

        for item in humidity.items:
            if check_condition(humidity_value, item.condition):
                humidity_icon = item.get_icon
                humidity_name = item.get_name
                break

        return humidity_name, humidity_icon

    def _get_uv_info(self, uv_index: int) -> tuple:
        """获取紫外线信息"""
        uv_category = self.loader.find_category_by_id(1011)
        uv_icon = "🔆"
        uv_name = "适中"

        for item in uv_category.items:
            if uv_index in item.level:
                uv_icon = item.get_icon
                uv_name = item.get_name
                break

        return uv_name, uv_icon

    def _get_visibility_info(self, visibility: int) -> tuple:
        """获取能见度信息"""
        visibility_category = self.loader.find_category_by_id(1013)
        visibility_icon = "👀"
        visibility_name = "良好"

        for item in visibility_category.items:
            if check_condition(visibility, item.condition):
                visibility_icon = item.get_icon
                visibility_name = item.get_name
                break

        return visibility_name, visibility_icon

    def generate_message(self, weather_data: Any, style: str = "romantic") -> str:
        """生成天气消息"""
        # 获取各种天气信息
        day_icon_item = self.loader.find_item_by_code(int(weather_data.iconDay))
        night_icon_item = self.loader.find_item_by_code(int(weather_data.iconNight))
        moon_icon_item = self.loader.find_item_by_code(int(weather_data.moonPhaseIcon))

        season_name, season_icon = self._get_season_info()
        humidity_name, humidity_icon = self._get_humidity_info(
            int(weather_data.humidity)
        )
        uv_name, uv_icon = self._get_uv_info(int(weather_data.uvIndex))
        visibility_name, visibility_icon = self._get_visibility_info(
            int(weather_data.vis)
        )

        # 准备模板数据
        template_data = {
            "date": weather_data.fxDate,
            "season": season_name,
            "season_icon": season_icon,
            "temp_min": weather_data.tempMin,
            "temp_max": weather_data.tempMax,
            "day_icon": day_icon_item.get_icon,
            "day_name": day_icon_item.get_name,
            "night_icon": night_icon_item.get_icon,
            "night_name": night_icon_item.get_name,
            "humidity_name": humidity_name,
            "humidity_icon": humidity_icon,
            "humidity": weather_data.humidity,
            "uv_name": uv_name,
            "uv_icon": uv_icon,
            "uv_index": weather_data.uvIndex,
            "precip": weather_data.precip,
            "vis_name": visibility_name,
            "vis_icon": visibility_icon,
            "vis": weather_data.vis,
            "sunrise": weather_data.sunrise,
            "sunset": weather_data.sunset,
            "moon_name": moon_icon_item.get_name,
            "moon_icon": moon_icon_item.get_icon,
            "moonrise": weather_data.moonrise,
            "moonset": weather_data.moonset,
        }

        # 选择模板风格
        selected_templates = self.templates.get(style, self.templates["romantic"])

        # 构建消息
        message_lines = [f"{self.header.choice.to_str}\n"]
        for template in selected_templates:
            try:
                line = template.format(**template_data)
                message_lines.append(line)
            except KeyError:
                # 如果某个字段缺失，跳过该行
                continue

        return "\n".join(message_lines)

    def generate_random_style_message(self, weather_data: Any) -> str:
        """随机选择风格生成消息"""
        styles = list(self.templates.keys())
        selected_style = random.choice(styles)
        return self.generate_message(weather_data, selected_style)


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
