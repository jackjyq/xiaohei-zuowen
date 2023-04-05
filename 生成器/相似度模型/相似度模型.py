# -*- coding: UTF-8 -*-
from abc import ABC, abstractmethod
import random


class 相似度模型类(ABC):
    @abstractmethod
    def __init__(self) -> None:
        """载入模型"""
        pass

    @abstractmethod
    def 计算特征向量(self, 文本: str):
        pass

    @abstractmethod
    def 计算相似度(self, 文本1: str, 文本2: str):
        pass


class random_similarity(相似度模型类):
    def __init__(self) -> None:
        print("random_similarity 相似度模型载入成功!")

    def 计算特征向量(self, 文本: str):
        return 0

    def 计算相似度(self, 文本1: str, 文本2: str) -> float:
        return random.random()


if __name__ == "__main__":
    相似度模型 = random_similarity()
    print(相似度模型.计算特征向量("你好"))
    print(相似度模型.计算相似度("你好", "小嘿作文生成器"))
