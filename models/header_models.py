import json
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Header:
    """头部模板"""

    header: str

    @property
    def to_str(self) -> str:
        return self.header


class HeaderDatabase:
    """头部消息数据"""

    def __init__(self):
        self._result: Optional[List[Header]] = []

    def load_from_json(self, data: Dict[str, Any]) -> "HeaderDatabase":
        """从JSON加载数据"""
        weather_headers = data.get("weather_headers")
        for header in weather_headers:
            obj = Header(header)
            self._result.append(obj)
        return self

    def load_from_file(self, file_path: str) -> "HeaderDatabase":
        """从JSON文件加载数据"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return self.load_from_json(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"文件不存在: {file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"文件格式错误: {file_path}")
        except Exception as e:
            raise RuntimeError(f"加载文件失败: {e}")

    @property
    def choice(self):
        """随机获取一个头部消息"""
        return random.choice(self._result)


if __name__ == "__main__":
    h = HeaderDatabase()
    h.load_from_file("../data/header.json")
    print(h.choice)
