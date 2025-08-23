import base64
import json
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from cryptography.hazmat.primitives import serialization

from settings.settings import settings


class ApiWeather(object):
    URL = "https://q64up3ryvx.re.qweatherapi.com/v7/weather/3d"
    METHOD = "GET"
    DESC = "和风天气API接口"
    TIMEOUT = 60

    @dataclass
    class Params:
        location: int = 101040500  # 重庆市江津区
        lang: str = "zh-hans"
        unit: str = "m"

        @property
        def to_dict(self):
            return asdict(self)

        @classmethod
        def load(cls):
            return cls()

    @dataclass
    class Headers:
        Authorization: str

        @property
        def to_dict(self):
            return asdict(self)

        @classmethod
        def load(cls):
            header = {"alg": "EdDSA", "kid": settings.CREDENTIALS_ID}

            # JWT载荷（Payload）
            payload = {
                "sub": settings.PROJECT_ID,  # 签发者
                "exp": int(time.time()) + 60 * 10,  # 过期时间（10分钟后）
                "iat": int(time.time()),  # 签发时间
            }

            # 对Header进行Base64URL编码
            header_json = json.dumps(header, separators=(",", ":"))
            header_encoded = (
                base64.urlsafe_b64encode(header_json.encode("utf-8"))
                .decode("utf-8")
                .rstrip("=")
            )

            # 对Payload进行Base64URL编码
            payload_json = json.dumps(payload, separators=(",", ":"))
            payload_encoded = (
                base64.urlsafe_b64encode(payload_json.encode("utf-8"))
                .decode("utf-8")
                .rstrip("=")
            )

            # 拼接Header和Payload
            signing_input = f"{header_encoded}.{payload_encoded}"

            # 加载私钥
            private_key = serialization.load_pem_private_key(
                settings.PRIVATE_KEY_PEM.encode("utf-8"),
                password=None,
            )

            # 使用Ed25519私钥对签名内容进行签名
            signature = private_key.sign(signing_input.encode("utf-8"))

            # 对签名结果进行Base64URL编码
            signature_encoded = (
                base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")
            )

            # 组合成最终的JWT Token
            jwt_token = f"Bearer {header_encoded}.{payload_encoded}.{signature_encoded}"

            return cls(jwt_token)

    @dataclass
    class Response:
        fxDate: str  # 预报日期
        sunrise: Optional[str]  # 日出时间，在高纬度地区可能为空
        sunset: Optional[str]  # 日落时间，在高纬度地区可能为空
        moonrise: Optional[str]  # 当天月升时间，可能为空
        moonset: Optional[str]  # 当天月落时间，可能为空
        moonPhase: Optional[str]  # 月相名称
        moonPhaseIcon: Optional[str]  # 月相图标代码，另请参考天气图标项目
        tempMax: Optional[str]  # 预报当天最高温度
        tempMin: Optional[str]  # 预报当天最低温度
        iconDay: Optional[str]  # 预报白天天气状况的图标代码，另请参考天气图标项目
        textDay: Optional[str]  # 预报白天天气状况文字描述，包括阴晴雨雪等天气状态的描述
        iconNight: Optional[str]  # 预报夜间天气状况的图标代码，另请参考天气图标项目
        textNight: Optional[
            str
        ]  # 预报晚间天气状况文字描述，包括阴晴雨雪等天气状态的描述
        wind360Day: Optional[str]  # 预报白天风向360角度
        windDirDay: Optional[str]  # 预报白天风向
        windScaleDay: Optional[str]  # 预报白天风力等级
        windSpeedDay: Optional[str]  # 预报白天风速，公里/小时
        wind360Night: Optional[str]  # 预报夜间风向360角度
        windDirNight: Optional[str]  # 预报夜间当天风向
        windScaleNight: Optional[str]  # 预报夜间风力等级
        windSpeedNight: Optional[str]  # 预报夜间风速，公里/小时
        precip: Optional[str]  # 预报当天总降水量，默认单位：毫米
        uvIndex: Optional[str]  # 紫外线强度指数
        humidity: Optional[str]  # 相对湿度，百分比数值
        pressure: Optional[str]  # 大气压强，默认单位：百帕
        vis: Optional[str]  # 能见度，默认单位：公里
        cloud: Optional[str]  # 云量，百分比数值。可能为空

        @property
        def to_dict(self):
            return asdict(self)

        @classmethod
        def load(cls, data: Dict[str, Any]) -> "ApiWeather.Response":
            return cls(**data)
