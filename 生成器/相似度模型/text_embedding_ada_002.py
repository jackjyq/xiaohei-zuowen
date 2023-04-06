# -*- coding: UTF-8 -*-
import pathlib
import sys

# 把生成器目录加入系统路径，以便该文件可被其它文件调用
生成器目录 = str(pathlib.Path(__file__).parent.parent)
if 生成器目录 not in sys.path:
    sys.path.insert(0, 生成器目录)

import os
from pathlib import Path

import openai
from dotenv import load_dotenv
from openai.embeddings_utils import cosine_similarity, get_embedding
from 数据库.数据库 import 数据库类
from 相似度模型.相似度模型 import 相似度模型类模版


class OpenaiApiKeyNotFoundException(Exception):
    pass


class text_embedding_ada_002(相似度模型类模版):
    # https://platform.openai.com/docs/guides/embeddings/use-cases
    def __init__(self) -> None:
        print(f"正在加载 text_embedding_ada_002 模型...")
        # 配置 API key
        self.脚本所在路径: Path = Path(__file__).parent
        配置文件路径: Path = self.脚本所在路径.parent / ".env"
        load_dotenv(配置文件路径)
        if not os.getenv("OPENAI_API_KEY"):
            raise OpenaiApiKeyNotFoundException(f"无法找到 OPENAI_API_KEY, 请检查 {配置文件路径}!")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.数据库 = 数据库类()
        print(f"text_embedding_ada_002 载入成功!")

    def 计算特征向量(self, 文本: str) -> list[float]:
        if 缓存特征向量 := self.数据库.读取特征向量_text_embedding_ada_002(文本):
            return 缓存特征向量
        # TODO https://platform.openai.com/docs/guides/rate-limits/retrying-with-exponential-backoff
        特征向量: list[float] = get_embedding(文本, engine="text-embedding-ada-002")
        self.数据库.插入特征向量_text_embedding_ada_002(文本, 特征向量)
        return 特征向量

    def 计算相似度(self, 向量1: list[float], 向量2: list[float]) -> float:
        return float(cosine_similarity(向量1, 向量2))


if __name__ == "__main__":
    相似度模型 = text_embedding_ada_002()
    向量1 = 相似度模型.计算特征向量("你好")
    向量2 = 相似度模型.计算特征向量("小嘿")
    相似度 = 相似度模型.计算相似度(向量1, 向量2)
    print(type(向量1[0]))
    print(相似度, type(相似度))
