# -*- coding: UTF-8 -*-
import pathlib
import sys
import os
from pathlib import Path

print("sbert_base_chinese_nli 模型加载中(1/2)...")
# https://stackoverflow.com/questions/62691279/how-to-disable-tokenizers-parallelism-true-false-warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from sentence_transformers import SentenceTransformer, util
from torch import Tensor
from numpy import ndarray

print("sbert_base_chinese_nli 模型载入成功(1/2)!")

# 把生成器目录加入系统路径，以便该文件可被其它文件调用
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from 相似度模型.相似度模型 import 相似度模型类


class sbert_base_chinese_nli(相似度模型类):
    # https://www.sbert.net/docs/quickstart.html
    def __init__(self) -> None:
        self.脚本所在路径: Path = Path(__file__).parent
        self.模型: SentenceTransformer = self._加载模型(
            self.脚本所在路径 / "sbert_base_chinese_nli_model"
        )

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

    def 计算特征向量(self, 文本: str) -> ndarray:
        return self.模型.encode(文本)

    def 计算相似度(self, 向量1: ndarray, 向量2: ndarray) -> float:
        return util.cos_sim(向量1, 向量2).item()


if __name__ == "__main__":
    相似度模型 = sbert_base_chinese_nli()
    向量1 = 相似度模型.计算特征向量("你好")
    向量2 = 相似度模型.计算特征向量("小嘿")
    相似度 = 相似度模型.计算相似度(向量1, 向量2)
    print(向量1)
    print(向量2)
    print(相似度)
