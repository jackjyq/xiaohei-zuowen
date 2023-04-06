# -*- coding: UTF-8 -*-
from abc import ABC, abstractmethod
import random


class 相似度模型类(ABC):
    @abstractmethod
    def __init__(self) -> None:
        """载入模型"""
        pass

    @abstractmethod
    def 计算特征向量(self, 文本: str) -> list[float]:
        pass

    @abstractmethod
    def 计算相似度(self, 向量1: list[float], 向量2: list[float]) -> float:
        pass


class random_similarity(相似度模型类):
    def __init__(self) -> None:
        print("random_similarity 模型载入成功!")

    def 计算特征向量(self, 文本: str) -> list[float]:
        return 0

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
