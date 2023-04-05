# -*- coding: UTF-8 -*-
import pathlib
import random
import sys
from dataclasses import dataclass, field
from typing import Any

# 把生成器目录加入系统路径，以便该文件可被其它文件调用
sys.path.append(str(pathlib.Path(__file__).parent))

from 相似度模型.相似度模型 import random_similarity
from 素材库.素材库 import 素材库类


@dataclass
class 作文类:
    文章: list[str] = field(default_factory=list)
    段数: int = 0
    字数: int = 0
    谓语: str = ""
    宾语: str = ""


class 生成器类:
    def __init__(self) -> None:
        self.相似度模型 = random_similarity()
        素材库实例 = 素材库类()
        素材库: dict[str, dict[str, list[Any]]] = 素材库实例.获取素材库()
        self.示例库: list[str] = 素材库["示例库"]["主题词示例"]
        self.模版库: dict[str, list[str]] = 素材库["模版库"]
        self.语料库: dict[str, dict[str, Any]] = self._计算语料库特征向量(素材库["语料库"])

    def _计算语料库特征向量(self, 语料库: dict[str, list[str]]) -> dict[str, dict[str, Any]]:
        """在语料库上添加特征向量
        输入格式:
            语料库 = {
                语料类别: [
                    语料
                ]
            }
        输出格式:
            语料库 = {
                语料类别: {
                    语料: 特征向量
                }
            }
        """

        def 移除主题词占位符(语料: str) -> str:
            语料 = 语料.replace("「主题宾语」", "")
            语料 = 语料.replace("「主题宾语」", "")
            return 语料

        print("正在计算语料库的特征向量...")
        语料与向量库: dict[str, dict[str, Any]] = {}
        # TODO: 增加进度条
        for 语料类别 in 语料库.keys():
            语料与向量列表: dict[str, Any] = {}
            for 语料 in 语料库[语料类别]:
                语料与向量列表[语料] = self.相似度模型.计算特征向量(移除主题词占位符(语料))
            语料与向量库[语料类别] = 语料与向量列表
        return 语料与向量库

    def _生成专用语料库(
        self,
        主题谓语: str,
        主题宾语: str,
        语料库: dict[str, dict[str, Any]],
    ) -> dict[str, list[tuple[str, Any]]]:
        """生成针对该主题词的专用语料库，语料库输出格式：
        专用语料库 = {
            语料类别: [(语料, 相似度)]
        }
        """

        def 计算语料及相似度(
            主题词: str, 语料及特征向量: dict[str, Any], 计算相似度并排序: bool
        ) -> list[tuple[str, Any]]:
            """
            计算相似度并排序 = True:
                由 {语料: 特征向量 } 转换为 [(语料, 相似度)]，并根据相似度排序
            计算相似度并排序 = False:
                由 {语料: 特征向量 } 转换为 [(语料, 0)]，不排序
            """
            语料及相似度: dict[str, Any] = {}
            if 计算相似度并排序:
                主题词特征向量 = self.相似度模型.计算特征向量(主题词)
                for 语料, 特征向量 in 语料及特征向量.items():
                    相似度 = self.相似度模型.计算相似度(主题词特征向量, 特征向量)
                    语料及相似度[语料] = 相似度
                return sorted(语料及相似度.items(), key=lambda item: item[1], reverse=True)
            else:
                return [(语料, 0) for 语料 in 语料及特征向量.keys()]

        专用语料库: dict[str, list[tuple[str, Any]]] = {}
        for 语料类别 in 语料库.keys():
            # 计算相似度、排序、并裁剪语料
            if 语料类别 == "事例":
                专用语料库[语料类别] = 计算语料及相似度(f"{主题谓语}{主题宾语}", 语料库[语料类别], 计算相似度并排序=True)[:30]
            elif 语料类别 == "名言":
                专用语料库[语料类别] = 计算语料及相似度(f"{主题谓语}{主题宾语}", 语料库[语料类别], 计算相似度并排序=True)[:10]
            else:
                # 对其他类别，仅更改格式
                专用语料库[语料类别] = 计算语料及相似度(f"{主题谓语}{主题宾语}", 语料库[语料类别], 计算相似度并排序=False)
            # 全部语料随机排列
            random.shuffle(专用语料库[语料类别])
        return 专用语料库

    def _替换语料(
        self, 文章: list[str], 专用语料库: dict[str, list[tuple[str, Any]]]
    ) -> list[str]:
        for 语料类别 in 专用语料库.keys():
            待替换词 = f"「{语料类别}」"
            语料索引 = 0
            for 段数 in range(len(文章)):
                while 文章[段数].find(待替换词) >= 0:
                    # 若存在待替换词
                    文章[段数] = 文章[段数].replace(待替换词, 专用语料库[语料类别][语料索引][0], 1)
                    语料索引 += 1
        return 文章

    def _替换主题词(self, 文章: list[str], 主题谓语: str, 主题宾语: str) -> list[str]:
        for 段数 in range(len(文章)):
            文章[段数] = 文章[段数].replace("「主题谓语」", 主题谓语)
            文章[段数] = 文章[段数].replace("「主题宾语」", 主题宾语)
        return 文章

    def 生成作文(self, 主题谓语: str = "", 主题宾语: str = "") -> 作文类:
        # 第一步：选择模版
        文章: list[str] = random.choice(list(self.模版库.values())).copy()
        # 第一步：替换语料
        专用语料库: dict[str, list[tuple[str, Any]]] = self._生成专用语料库(主题谓语, 主题宾语, self.语料库)
        文章 = self._替换语料(文章, 专用语料库)
        # 第三步：替换主题词
        文章 = self._替换主题词(文章, 主题谓语, 主题宾语)
        # 第四步: 生成统计信息
        段数 = len(文章)
        字数 = sum(len(段落) for 段落 in 文章)
        return 作文类(文章=文章, 段数=段数, 字数=字数, 谓语=主题谓语, 宾语=主题宾语)


# 命令行界面
if __name__ == "__main__":
    生成器: 生成器类 = 生成器类()
    print("欢迎使用小嘿作文生成器！按 Ctrl+C 退出。")
    print("主题词示例：")
    print(", ".join([示例[0] + "|" + 示例[1] for 示例 in 生成器.示例库]))
    while True:
        print()
        谓语 = input("请输入主题谓语: ")
        宾语 = input("请输入主题宾语: ")
        作文: 作文类 = 生成器.生成作文(谓语, 宾语)
        print(作文.谓语 + 作文.宾语)
        for 段落 in 作文.文章:
            print(段落)
        print(f"（共 {作文.段数} 段，{作文.字数} 字）")
