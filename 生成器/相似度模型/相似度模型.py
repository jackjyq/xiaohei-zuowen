# -*- coding: UTF-8 -*-
from abc import ABC, abstractmethod


class 相似度模型类模版(ABC):
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
