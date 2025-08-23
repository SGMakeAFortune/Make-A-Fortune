import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional


class AnniversaryStyle(Enum):
    DETAILED = "detailed"  # 详细统计风格
    ROMANTIC = "romantic"  # 浪漫抒情风格
    CUTE = "cute"  # 可爱卡通风格
    POETIC = "poetic"  # 诗意文学风格
    FUNNY = "funny"  # 幽默搞笑风格
    MILESTONE = "milestone"  # 里程碑风格


class AnniversaryCalculator:
    """纪念日计算器"""

    @staticmethod
    def calculate_anniversaries(
        start_date: datetime, current_date: datetime = None
    ) -> Dict[str, Dict]:
        """
        计算各种纪念日
        """
        if current_date is None:
            current_date = datetime.now()

        total_days = (current_date - start_date).days
        if total_days < 0:
            return {"error": "开始日期不能晚于当前日期"}

        return {
            "total_days": total_days,
            "daily": AnniversaryCalculator._get_daily_info(total_days),
            "weekly": AnniversaryCalculator._get_weekly_info(total_days),
            "monthly": AnniversaryCalculator._get_monthly_info(
                start_date, current_date
            ),
            "yearly": AnniversaryCalculator._get_yearly_info(start_date, current_date),
            "special": AnniversaryCalculator._get_special_anniversaries(total_days),
            "next_anniversary": AnniversaryCalculator._get_next_anniversary(
                start_date, current_date
            ),
            "love_score": AnniversaryCalculator._calculate_love_score(total_days),
        }

    @staticmethod
    def _calculate_love_score(days: int) -> int:
        """计算爱情分数"""
        base_score = min(100, days // 10)
        bonus = min(50, days // 100 * 10)
        return min(100, base_score + bonus)

    @staticmethod
    def _get_daily_info(total_days: int) -> Dict:
        """获取每日信息"""
        return {
            "days": total_days,
            "weeks": total_days // 7,
            "remaining_days": total_days % 7,
            "message": f"已经相识 {total_days} 天",
        }

    @staticmethod
    def _get_weekly_info(total_days: int) -> Dict:
        """获取每周信息"""
        weeks = total_days // 7
        remaining_days = total_days % 7

        return {
            "weeks": weeks,
            "remaining_days": remaining_days,
            "message": f"已经相识 {weeks} 周 {remaining_days} 天",
        }

    @staticmethod
    def _get_monthly_info(start_date: datetime, current_date: datetime) -> Dict:
        """获取每月信息"""
        # 计算完整的月数
        months = (current_date.year - start_date.year) * 12 + (
            current_date.month - start_date.month
        )

        # 调整如果当前日小于开始日
        if current_date.day < start_date.day:
            months -= 1

        # 计算下一个整月纪念日
        next_month_date = start_date + timedelta(days=30 * (months + 1))
        days_until_next_month = (next_month_date - current_date).days

        return {
            "months": months,
            "message": f"已经相识 {months} 个月",
            "next_month_days": max(0, days_until_next_month),
        }

    @staticmethod
    def _get_yearly_info(start_date: datetime, current_date: datetime) -> Dict:
        """获取每年信息"""
        years = current_date.year - start_date.year

        # 调整如果还没到周年日
        if (current_date.month, current_date.day) < (start_date.month, start_date.day):
            years -= 1

        # 计算下一个周年日
        next_year_date = datetime(current_date.year, start_date.month, start_date.day)
        if next_year_date < current_date:
            next_year_date = datetime(
                current_date.year + 1, start_date.month, start_date.day
            )

        days_until_next_year = (next_year_date - current_date).days

        return {
            "years": years,
            "message": f"已经相识 {years} 年",
            "next_year_days": max(0, days_until_next_year),
        }

    @staticmethod
    def _get_special_anniversaries(total_days: int) -> List[Dict]:
        """获取特殊纪念日"""
        special_days = [7, 14, 30, 100, 365, 500, 730, 1000, 1825, 3650, 10000]

        anniversaries = []
        for day in special_days:
            if total_days >= day:
                anniversaries.append(
                    {
                        "days": day,
                        "type": "past",
                        "message": f"第 {day} 天纪念日 ({AnniversaryCalculator._format_special_day(day)})",
                    }
                )
            else:
                anniversaries.append(
                    {
                        "days": day,
                        "type": "future",
                        "days_until": day - total_days,
                        "message": f"距离第 {day} 天纪念日还有 {day - total_days} 天",
                    }
                )

        return anniversaries

    @staticmethod
    def _format_special_day(days: int) -> str:
        """格式化特殊纪念日名称"""
        special_names = {
            7: "一周",
            14: "两周",
            30: "一个月",
            100: "百日",
            365: "一周年",
            500: "五百天",
            730: "两周年",
            1000: "千日",
            1825: "五周年",
            3650: "十周年",
            10000: "万日",
        }
        return special_names.get(days, f"{days}天")

    @staticmethod
    def _get_next_anniversary(start_date: datetime, current_date: datetime) -> Dict:
        """获取下一个重要纪念日"""
        total_days = (current_date - start_date).days

        # 检查特殊纪念日
        special_days = [7, 14, 30, 100, 365, 500, 730, 1000, 1825, 3650, 10000]
        for day in special_days:
            if day > total_days:
                return {
                    "type": "special",
                    "days": day,
                    "days_until": day - total_days,
                    "message": f"距离第 {day} 天纪念日还有 {day - total_days} 天",
                }

        # 检查月纪念日
        next_month_date = start_date + timedelta(days=30 * (total_days // 30 + 1))
        days_until_month = (next_month_date - current_date).days

        # 检查年纪念日
        next_year_date = datetime(current_date.year, start_date.month, start_date.day)
        if next_year_date < current_date:
            next_year_date = datetime(
                current_date.year + 1, start_date.month, start_date.day
            )
        days_until_year = (next_year_date - current_date).days

        if days_until_month < days_until_year:
            return {
                "type": "monthly",
                "days_until": days_until_month,
                "message": f"距离下个月纪念日还有 {days_until_month} 天",
            }
        else:
            return {
                "type": "yearly",
                "days_until": days_until_year,
                "message": f"距离周年纪念日还有 {days_until_year} 天",
            }


class AnniversaryMessageGenerator:
    """纪念日消息生成器"""

    @staticmethod
    def _get_style_weights() -> Dict[AnniversaryStyle, int]:
        """根据天数获取样式权重"""
        weights = {
            AnniversaryStyle.DETAILED: 20,
            AnniversaryStyle.ROMANTIC: 20,
            AnniversaryStyle.CUTE: 20,
            AnniversaryStyle.POETIC: 20,
            AnniversaryStyle.FUNNY: 20,
            AnniversaryStyle.MILESTONE: 20,
        }

        return weights

    @staticmethod
    def generate_anniversary_message(
        start_date: datetime,
        current_date: datetime = None,
        style: Optional[AnniversaryStyle] = None,
    ) -> str:
        """
        生成纪念日消息，可指定样式或随机选择
        """
        if current_date is None:
            current_date = datetime.now()

        anniversaries = AnniversaryCalculator.calculate_anniversaries(
            start_date, current_date
        )
        if "error" in anniversaries:
            return anniversaries["error"]

        # 随机选择样式
        if style is None:
            weights = AnniversaryMessageGenerator._get_style_weights()
            styles = list(weights.keys())
            weight_values = [weights[s] for s in styles]
            style = random.choices(styles, weights=weight_values, k=1)[0]

        # 根据样式生成消息
        if style == AnniversaryStyle.DETAILED:
            return AnniversaryMessageGenerator._detailed_style(
                start_date, current_date, anniversaries
            )
        elif style == AnniversaryStyle.ROMANTIC:
            return AnniversaryMessageGenerator._romantic_style(
                start_date, current_date, anniversaries
            )
        elif style == AnniversaryStyle.CUTE:
            return AnniversaryMessageGenerator._cute_style(
                start_date, current_date, anniversaries
            )
        elif style == AnniversaryStyle.POETIC:
            return AnniversaryMessageGenerator._poetic_style(
                start_date, current_date, anniversaries
            )
        elif style == AnniversaryStyle.FUNNY:
            return AnniversaryMessageGenerator._funny_style(start_date, anniversaries)
        elif style == AnniversaryStyle.MILESTONE:
            return AnniversaryMessageGenerator._milestone_style(
                start_date, anniversaries
            )
        else:
            return AnniversaryMessageGenerator._detailed_style(
                start_date, current_date, anniversaries
            )

    @staticmethod
    def _detailed_style(
        start_date: datetime, current_date: datetime, anniversaries: Dict
    ) -> str:
        """详细统计风格"""
        messages = [
            "💕 我们的纪念日统计 💕",
            "═" * 15,
            f"📅 相识日期: {start_date.strftime('%Y年%m月%d日')}",
            f"📅 今天日期: {current_date.strftime('%Y年%m月%d日')}",
            "",
            f"✨ 总天数: {anniversaries['total_days']} 天",
            f"📆 {anniversaries['weekly']['message']}",
            f"🌙 {anniversaries['monthly']['message']}",
            f"🎉 {anniversaries['yearly']['message']}",
            "",
            "🎯 下一个纪念日:",
            f"   {anniversaries['next_anniversary']['message']}",
            "",
            "🌟 爱情指数:",
            f"   💖 {anniversaries['love_score']}/100 分",
        ]
        return "\n".join(messages)

    @staticmethod
    def _romantic_style(
        start_date: datetime, current_date: datetime, anniversaries: Dict
    ) -> str:
        """浪漫抒情风格"""
        days = anniversaries["total_days"]
        messages = [
            "🌹 致我最爱的人 🌹",
            "❤️" * 15,
            f"从 {start_date.strftime('%Y年%m月%d日')} 开始",
            f"到 {current_date.strftime('%Y年%m月%d日')} 的此刻",
            "",
            f"我们已经相爱 {days} 个日夜",
            f"相当于 {days // 30} 个月 {days % 30} 天的浪漫",
            f"也就是 {days // 365} 年 {(days % 365) // 30} 个月的甜蜜",
            "",
            "💝 我们的爱情就像:",
            f"   {AnniversaryMessageGenerator._get_romantic_analogy()}",
            "",
            "🌈 每一天都因为有你而更加美好",
            "✨ 期待我们的每一个明天",
        ]
        return "\n".join(messages)

    @staticmethod
    def _cute_style(
        start_date: datetime, current_date: datetime, anniversaries: Dict
    ) -> str:
        """可爱卡通风格"""
        days = anniversaries["total_days"]
        messages = [
            "🐰🎀 纪念日小贴士 🎀🐰",
            "🌸" * 20,
            f"📅 开始日期: {start_date.strftime('%Y.%m.%d')}",
            f"⏰ 今天日期: {current_date.strftime('%Y.%m.%d')}",
            "",
            f"🐾 我们已经一起: {days} 天啦！",
            f"🦄 相当于: {days // 7} 周 {days % 7} 天",
            f"🍰 月亮姐姐见证了我们: {days // 30} 个月",
            "",
            "🎁 下一个惊喜日:",
            f"   🎯 {anniversaries['next_anniversary']['message']}",
            "",
            "💫 爱情魔法值:",
            f"   ✨ {anniversaries['love_score']}% 充满魔力！",
        ]
        return "\n".join(messages)

    @staticmethod
    def _poetic_style(
        start_date: datetime, current_date: datetime, anniversaries: Dict
    ) -> str:
        """诗意文学风格"""
        days = anniversaries["total_days"]
        messages = [
            "📜 时光的诗篇 📜",
            "──────────────",
            f"初遇于 {start_date.strftime('%Y年%m月%d日')}",
            f"相守至 {current_date.strftime('%Y年%m月%d日')}",
            "",
            f"🌅 {days} 个日出日落",
            f"🌙 {days // 30} 回月圆月缺",
            f"🎋 {days // 365} 度春夏秋冬",
            "",
            "💞 情如:",
            f"   {AnniversaryMessageGenerator._get_poetic_metaphor()}",
            "",
            "🎑 愿时光静好，与君语",
            "🌌 愿细水流年，与君同",
        ]
        return "\n".join(messages)

    @staticmethod
    def _funny_style(start_date: datetime, anniversaries: Dict) -> str:
        """幽默搞笑风格"""
        days = anniversaries["total_days"]
        messages = [
            "😂 爱情生存报告 😂",
            "🎪" * 15,
            f"从 {start_date.strftime('%Y年%m月%d日')} 开始",
            f"你已经被我'烦'了 {days} 天！",
            "",
            f"📊 生存数据:",
            f"   🎯 忍耐等级: {min(100, days // 10)}/100",
            f"   😜 搞笑次数: {days * 3} 次",
            f"   🍔 一起吃饭: {days * 2} 顿",
            "",
            "🏆 成就解锁:",
            f"   ✅ 成功相处 {days} 天",
            f"   🎉 下一个成就: {anniversaries['next_anniversary']['message']}",
            "",
            "💕 总结: 继续互相'伤害'吧！",
        ]
        return "\n".join(messages)

    @staticmethod
    def _milestone_style(start_date: datetime, anniversaries: Dict) -> str:
        """里程碑风格"""
        days = anniversaries["total_days"]
        messages = [
            "🏆 爱情里程碑 🏆",
            "⭐" * 20,
            f"🎯 总成就点数: {days}",
            f"📅 旅程开始: {start_date.strftime('%Y.%m.%d')}",
            "",
            "🎖️ 已达成里程碑:",
            f"   ✅ 第一周 ({7 if days >= 7 else '进行中'})",
            f"   ✅ 第一个月 ({30 if days >= 30 else '进行中'})",
            f"   ✅ 第一百天 ({100 if days >= 100 else '进行中'})",
            f"   ✅ 第一年 ({365 if days >= 365 else '进行中'})",
            "",
            "🔜 下一个里程碑:",
            f"   🎯 {anniversaries['next_anniversary']['message']}",
            "",
            "💫 爱情能量值:",
            f"   ✨ {anniversaries['love_score']}/100",
        ]
        return "\n".join(messages)

    @staticmethod
    def _get_romantic_analogy() -> str:
        """获取浪漫比喻"""
        analogies = [
            "初生的朝阳，充满希望和温暖",
            "绽放的花朵，美丽而芬芳",
            "成熟的果实，甜蜜而充实",
            "陈年的美酒，越久越香醇",
            "永恒的星辰，闪耀而持久",
            "深海的珍珠，珍贵而难得",
            "山间的清泉，纯净而甘甜",
        ]
        return random.choice(analogies)

    @staticmethod
    def _get_poetic_metaphor() -> str:
        """获取诗意比喻"""
        metaphors = [
            "长河流水，绵延不绝",
            "青山不改，绿水长流",
            "明月清风，相伴永远",
            "琴瑟和鸣，岁月静好",
            "花开并蒂，莲生同心",
            "云卷云舒，不离不弃",
            "星辰大海，共赴前程",
        ]
        return random.choice(metaphors)
