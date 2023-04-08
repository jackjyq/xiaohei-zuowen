import re
from pathlib import Path
from pprint import pprint
from typing import Any
import editdistance


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

    @staticmethod
    def 检查语料库(语料库: dict[str, list[str]]):
        """检查语料库，并打印结果
        检查语料列表(素材库实例.获取素材库()['语料库'])
        """
        for 语料类别 in 语料库.keys():
            print(f"\n{语料类别} 检查报告:\n")
            for i in range(len(语料库[语料类别])):
                语料: str = 语料库[语料类别][i]
                # 检查非法标点
                for 字符 in 语料:
                    if 字符 in ",.\"':?!":
                        print(f"第 {i+1} 行存在英文标点 {字符}：{语料}")
                    if 字符 in "[]【】()（）{}*":
                        print(f"第 {i+1} 行存在非法标点 {字符}：{语料}")
                # 检查句末标点
                if 语料[-1] not in "。！？":
                    print(f"第 {i+1} 行未以。？！结尾：{语料}")
                # 检查方引号配对
                待查语料 = 语料.replace("「主题谓语」", "").replace("「主题宾语」", "")
                if "「" in 待查语料 or "」" in 待查语料:
                    print(f"第 {i+1} 行有未配对方引号：{语料}")
                # 检查相似语料
                for j in range(i):
                    if (
                        (语料 in 语料库[语料类别][j])
                        or (语料库[语料类别][j] in 语料)
                        or (editdistance.eval(语料, 语料库[语料类别][j]) < 4)
                    ):
                        print(f"第 {i+1} 行与第 {j+1} 行相似：{语料}")


if __name__ == "__main__":
    素材库实例 = 素材库类()
    素材库 = 素材库实例.获取素材库()
    # pprint(素材库, indent=2)
    素材库类.检查语料库(素材库["语料库"])
