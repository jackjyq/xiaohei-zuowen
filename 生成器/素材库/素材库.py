import re
from pathlib import Path
from pprint import pprint
from typing import Any


class 素材库类:
    def __init__(self, 路径: Path = Path(__file__).parent) -> None:
        self.脚本所在路径 = 路径

    def _获取子类列表(self, 大类路径: Path) -> list[str]:
        return [
            文件.stem for 文件 in 大类路径.iterdir() if 文件.is_file() and 文件.suffix == ".txt"
        ]

    def _获取素材列表(self, 子类路径: Path) -> list[str]:
        with open(子类路径, "r") as 文件:
            # 去掉多余的换行符，跳过空行
            return [行.strip() for 行 in 文件.readlines() if 行.strip()]

    def _获取大类字典(self, 大类: str) -> dict[str, list[str]]:
        大类字典: dict[str, list[str]] = {}
        for 子类 in self._获取子类列表(self.脚本所在路径 / 大类):
            大类字典[子类] = self._获取素材列表((self.脚本所在路径 / 大类 / 子类).with_suffix(".txt"))
        return 大类字典

    def 获取素材库(self) -> dict[str, dict[str, list[Any]]]:
        """素材库格式
        素材库 = {
            "模版库": {
                子类: [段落, ...],
            },
            "语料库": {
                子类: [语料, ...],
            },
            "示例库": {
                子类: [(主题谓语, 主题宾语), ...],
            },
            ...
        }
        """
        # 获取示例列表
        示例列表: list[tuple] = []
        for 行 in self._获取大类字典("示例库")["主题词示例"]:
            if 匹配 := re.match(r"「(\w+)」「(\w+)」", 行):
                示例列表.append(匹配.groups())
        # 生成素材库
        素材库: dict[str, dict[str, list[Any]]] = {
            "模版库": self._获取大类字典("模版库"),
            "语料库": self._获取大类字典("语料库"),
            "示例库": {"主题词示例": 示例列表},
        }
        return 素材库

    def 检查素材库(self) -> bool:
        # TODO: 检查素材库质量，是否重复等
        return True


if __name__ == "__main__":
    素材库实例 = 素材库类()
    pprint(素材库实例.获取素材库(), indent=2)
