# -*- coding: UTF-8 -*-
import pathlib
import sys

# 把生成器目录加入系统路径，以便该文件可被其它文件调用
生成器目录 = str(pathlib.Path(__file__).parent.parent)
if 生成器目录 not in sys.path:
    sys.path.insert(0, 生成器目录)

import os
from pathlib import Path

print("sbert_base_chinese_nli 模型加载中(1/2)...")
# https://stackoverflow.com/questions/62691279/how-to-disable-tokenizers-parallelism-true-false-warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from sentence_transformers import SentenceTransformer, util

print("sbert_base_chinese_nli 模型载入成功(1/2)!")
from 相似度模型.相似度模型 import 相似度模型类模版
from 数据库.数据库 import 数据库类


class sbert_base_chinese_nli(相似度模型类模版):
    # https://www.sbert.net/docs/quickstart.html
    def __init__(self) -> None:
        self.脚本所在路径: Path = Path(__file__).parent
        self.模型: SentenceTransformer = self._加载模型(
            self.脚本所在路径 / "sbert_base_chinese_nli_model"
        )
        self.模型.max_seq_length = 512
        self.数据库 = 数据库类()

    def _加载模型(self, 模型路径: Path) -> SentenceTransformer:
        if os.path.exists(模型路径):
            print(f"正在从 {模型路径} 加载 sbert_base_chinese_nli 模型(2/2)...")
            模型: SentenceTransformer = SentenceTransformer(模型路径)
        else:
            print(f"正在下载 sbert_base_chinese_nli 模型(2/2)...")
            # https://huggingface.co/uer/sbert-base-chinese-nli
            模型 = SentenceTransformer("uer/sbert-base-chinese-nli")
            模型.save(模型路径)
        print("sbert_base_chinese_nli 模型载入成功(2/2)!")
        return 模型

    def 计算特征向量(self, 文本: str) -> list[float]:
        if 缓存特征向量 := self.数据库.读取特征向量_sbert_base_chinese_nli(文本):
            return 缓存特征向量
        特征向量: list[float] = self.模型.encode(文本).tolist()
        self.数据库.插入特征向量_sbert_base_chinese_nli(文本, 特征向量)
        return 特征向量

    def 计算相似度(self, 向量1: list[float], 向量2: list[float]) -> float:
        return util.cos_sim(向量1, 向量2).item()


if __name__ == "__main__":
    相似度模型 = sbert_base_chinese_nli()
    向量1 = 相似度模型.计算特征向量("你好")
    向量2 = 相似度模型.计算特征向量("小嘿")
    相似度 = 相似度模型.计算相似度(向量1, 向量2)
    print(向量1)
    print(向量2)
    print(相似度)
