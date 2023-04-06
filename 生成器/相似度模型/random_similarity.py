# -*- coding: UTF-8 -*-
import pathlib
import sys

# 把生成器目录加入系统路径，以便该文件可被其它文件调用
生成器目录 = str(pathlib.Path(__file__).parent.parent)
if 生成器目录 not in sys.path:
    sys.path.insert(0, 生成器目录)
import random

from 相似度模型.相似度模型 import 相似度模型类模版


class random_similarity(相似度模型类模版):
    def __init__(self) -> None:
        print("random_similarity 模型载入成功!")

    def 计算特征向量(self, 文本: str) -> list[float]:
        return [0]

    def 计算相似度(self, 向量1: list[float], 向量2: list[float]) -> float:
        return random.random()


if __name__ == "__main__":
    相似度模型 = random_similarity()
    向量1 = 相似度模型.计算特征向量("你好")
    向量2 = 相似度模型.计算特征向量("小嘿")
    相似度 = 相似度模型.计算相似度(向量1, 向量2)
    print(向量1)
    print(向量2)
    print(相似度)
