from dataclasses import dataclass
from typing import Any, Dict, List, Optional


class ApiDailySentence:
    URL = "https://open.iciba.com/dsapi/"
    METHOD = "GET"
    DESC = "金山词霸每日金句API"
    TIMEOUT = 60

    @dataclass
    class Response:
        content: Optional[str]
        note: Optional[str]
        sid: Optional[str]
        tts: Optional[str]
        love: Optional[str]
        translation: Optional[str]
        picture: Optional[str]
        picture2: Optional[str]
        caption: Optional[str]
        dateline: Optional[str]
        s_pv: Optional[str]
        sp_pv: Optional[str]
        fenxiang_img: Optional[str]
        picture3: Optional[str]
        picture4: Optional[str]
        tags: Optional[List]

        @classmethod
        def load(cls, data: Dict[str, Any]) -> "ApiDailySentence.Response":
            print(data)
            return cls(**data)

        @property
        def to_str(self) -> str:
            return f"每日一句：\n{self.content}\n{self.note}"
