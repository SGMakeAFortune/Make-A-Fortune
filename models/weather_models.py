import json
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class WeatherItem:
    """天气项目数据类"""

    name: str
    icons: List[str]
    code: Optional[int] = None
    condition: Optional[str] = None
    level: Optional[List[int]] = None

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "WeatherItem":
        """解析数据"""
        return cls(
            name=data["name"],
            icons=data["icons"],
            code=data.get("code"),
            condition=data.get("condition"),
            level=data.get("level"),
        )

    @property
    def choices(self) -> str:
        return random.choice(self.icons)


@dataclass
class WeatherCategory:
    """天气类别数据类"""

    id: int
    name: str
    items: List[WeatherItem]

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "WeatherCategory":
        """解析数据"""
        items = [WeatherItem.load(item_data) for item_data in data["items"]]
        return cls(id=data["id"], name=data["name"], items=items)


class WeatherDataLoader:
    """天气数据加载器"""

    def __init__(self):
        self._categories: Dict[str, WeatherCategory] = {}
        self._code_index: Dict[int, WeatherItem] = {}
        self._category_id_index: Dict[int, WeatherCategory] = {}
        self._name_index: Dict[str, List[WeatherItem]] = {}

    def _build_indexes(self) -> None:
        """构建索引以加速查询"""
        self._code_index.clear()
        self._category_id_index.clear()
        self._name_index.clear()

        for category in self._categories.values():
            # 构建类别ID索引
            self._category_id_index[category.id] = category

            # 构建代码和名称索引
            for item in category.items:
                if item.code is not None:
                    self._code_index[item.code] = item

                if item.name not in self._name_index:
                    self._name_index[item.name] = []
                self._name_index[item.name].append(item)

    def load_categories(self, data: Dict[str, Any]) -> None:
        """加载所有天气类别数据"""
        for category_key, category_data in data.get("weather_categories", {}).items():
            self._categories[category_key] = WeatherCategory.load(category_data)
        self._build_indexes()

    def load_from_file(self, file_path: str) -> None:
        """从JSON文件加载天气数据"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.load_categories(data)
        except FileNotFoundError:
            raise FileNotFoundError(f"文件不存在: {file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"文件格式错误: {file_path}")
        except Exception as e:
            raise RuntimeError(f"加载文件失败: {e}")

    def find_item_by_code(self, code: int) -> Optional[WeatherItem]:
        """通过code查找天气项目"""
        return self._code_index.get(code)

    def find_category_by_id(self, category_id: int) -> Optional[WeatherCategory]:
        """根据ID查找类别"""
        return self._category_id_index.get(category_id)

    def find_items_by_name(self, name: str) -> List[WeatherItem]:
        """通过名称查找天气项目"""
        return self._name_index.get(name, [])

    def get_category(self, category_key: str) -> Optional[WeatherCategory]:
        """根据类别名称获取类别"""
        return self._categories.get(category_key)

    @property
    def get_all(self) -> Dict[str, WeatherCategory]:
        """获取所有天气类别"""
        return self._categories.copy()


if __name__ == "__main__":
    # 创建加载器实例
    loader = WeatherDataLoader()
