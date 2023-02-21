# -*- coding: UTF-8 -*-
import copy
import random
import re
import sqlite3
from dataclasses import dataclass, field
from os import listdir, path, environ
from typing import List, Dict, Tuple

# https://www.sbert.net/docs/quickstart.html
print("正在导入 SentenceTransformer...")
# https://stackoverflow.com/questions/62691279/how-to-disable-tokenizers-parallelism-true-false-warning
environ["TOKENIZERS_PARALLELISM"] = "false"
from sentence_transformers import SentenceTransformer, util


@dataclass
class 作文类:
    文章: List[str] = field(default_factory=list)
    段数: int = 0
    字数: int = 0
    谓语: str = ""
    宾语: str = ""


class 生成器类:
    def __init__(self, 随机种子: int = None) -> None:
        random.seed(随机种子)
        self.基础路径 = path.abspath(path.dirname(__file__))
        # 读取模板库
        self.模版库 = {}
        self.模版列表 = self.获取列表(self.基础路径 + "/模版库")
        for 模版名称 in self.模版列表:
            self.模版库[模版名称] = self.读取文件(self.基础路径 + "/模版库/" + 模版名称 + ".txt")
        self.语料列表 = self.获取列表(self.基础路径 + "/语料库")
        # 读取语料库
        self.语料库 = {}
        for 语料名称 in self.语料列表:
            self.语料库[语料名称] = self.读取文件(self.基础路径 + "/语料库/" + 语料名称 + ".txt")
        self.语料库拷贝 = copy.deepcopy(self.语料库)
        # 读取示例库
        self.主题词示例: list[tuple] = []
        for 行 in self.读取文件(self.基础路径 + "/示例库/" + "主题词示例.txt"):
            if 匹配 := re.match(r"「(\w+)」「(\w+)」", 行):
                self.主题词示例.append(匹配.groups())
        self.作文总数 = self.计算作文总数()
        self.数据库 = 数据库类()
        self.模型: SentenceTransformer = self.加载模型(self.基础路径 + "/模型")
        self.特征向量库们: Dict[Dict] = self.计算特征向量()

    def 加载模型(self, 模型路径) -> SentenceTransformer:
        if path.exists(模型路径):
            print(f"正在加载 {模型路径} ...")
            return SentenceTransformer(模型路径)
        else:
            print(f"正在下载 uer/sbert-base-chinese-nli...")
            # https://huggingface.co/uer/sbert-base-chinese-nli
            模型 = SentenceTransformer("uer/sbert-base-chinese-nli")
            print(f"正在保存 {模型路径}...")
            模型.save(模型路径)
            return 模型

    def 计算特征向量(self) -> Dict:
        print("正在计算 素材的特征向量...")

        def 清洗语料(语料: str):
            语料 = 语料.replace("「主题谓语」", "")
            语料 = 语料.replace("「主题宾语」", "")
            return 语料

        return {
            "事例": {事例: self.模型.encode(清洗语料(事例)) for 事例 in self.语料库["事例"]},
            "名言": {名言: self.模型.encode(清洗语料(名言)) for 名言 in self.语料库["名言"]},
        }

    def 读取文件(self, 文件路径: str) -> list:
        数据 = []
        with open(文件路径, "r") as 文件:
            原始数据 = 文件.readlines()
            # 去掉多余的换行符
            for 行 in 原始数据:
                数据.append(行.strip())
        return 数据

    def 获取列表(self, 目录路径: str) -> list:
        语料名称 = []
        for 文件名 in listdir(目录路径):
            if 文件名.endswith(".txt"):
                语料名称.append(文件名[:-4])
        return 语料名称

    def 语料库洗牌(self, 主题词: str) -> None:
        for 语料名称 in self.语料列表:
            # 仅取最相似的前 N 个语料，N 的数量可以调整
            if 语料名称 == "事例":
                self.语料库拷贝["事例"] = self.根据相似度排序(主题词, self.特征向量库们["事例"])[:15]
            if 语料名称 == "名言":
                self.语料库拷贝["名言"] = self.根据相似度排序(主题词, self.特征向量库们["名言"])[:10]
            random.shuffle(self.语料库拷贝[语料名称])

    def 根据相似度排序(self, 主题词: str, 特征向量库: Dict) -> List[str]:
        主题词特征向量 = self.模型.encode(主题词)
        语料相似度: List[Tuple] = []
        for 语料, 语料特征向量 in 特征向量库.items():
            相似度 = util.cos_sim(主题词特征向量, 语料特征向量)
            语料相似度.append((语料, 相似度))
        return [x[0] for x in sorted(语料相似度, key=lambda x: x[1], reverse=True)]

    def 应用语料(self, 段落: str, 语料计数: dict, 语料名称: str) -> str:
        待替换词 = "「" + 语料名称 + "」"
        while 段落.find(待替换词) >= 0:
            # 若存在待替换词
            段落 = 段落.replace(待替换词, self.语料库拷贝[语料名称][语料计数[语料名称]], 1)
            语料计数[语料名称] += 1
        return 段落

    def 初始化语料计数(self) -> dict:
        语料计数 = {}
        for 语料名称 in self.语料列表:
            语料计数[语料名称] = 0
        return 语料计数

    def 生成作文(self, 主题谓语: str = "", 主题宾语: str = "") -> 作文类:
        # 随机选择模版
        模版 = random.choice(list(self.模版库.values()))
        # 随机替换语料
        初稿 = []
        # 初始化语料库拷贝
        self.语料库拷贝 = copy.deepcopy(self.语料库)
        self.语料库洗牌(主题谓语 + 主题宾语)
        语料计数 = self.初始化语料计数()
        for 段落 in 模版:
            for 语料名称 in self.语料列表:
                段落 = self.应用语料(段落, 语料计数, 语料名称)
            初稿.append(段落)
        # 替换主题词
        定稿 = []
        字数 = 0
        for 段落 in 初稿:
            段落 = 段落.replace("「主题谓语」", 主题谓语)
            段落 = 段落.replace("「主题宾语」", 主题宾语)
            字数 += len(段落)
            定稿.append(段落)
        # 记录数据库
        self.数据库.写入数据库(谓语=主题谓语, 宾语=主题宾语)
        return 作文类(文章=定稿, 段数=len(定稿), 字数=字数, 谓语=主题谓语, 宾语=主题宾语)

    def 生成记录(self) -> list:
        return self.数据库.读取数据库()

    def 计算作文总数(self) -> int:
        """计算能够生成的作文总数"""
        作文总数 = 0
        for 模版名称 in self.模版列表:
            作文总数 += self.计算模版作文总数(模版名称)
        return 作文总数

    def 计算模版作文总数(self, 模版名称: str) -> int:
        """计算针对某个模版能够生成的作文总数"""
        模版作文总数 = 1
        for 语料名称 in self.语料列表:
            # 计算语料在模版中的选择次数
            语料选择次数 = 0
            for 模版段落 in self.模版库[模版名称]:
                语料选择次数 += 模版段落.count("「" + 语料名称 + "」")
            # 计算语料数量
            语料数量 = len(self.语料库[语料名称])
            # 计算某语料所贡献的作文数量
            for i in range(语料选择次数):
                模版作文总数 *= 语料数量 - i
        return 模版作文总数


class 数据库类:
    def __init__(self) -> None:
        # 初始化数据库
        # 谓语 宾语 生成次数
        # 勇于 尝试 10
        # 积极 进去 2
        self.基础路径 = path.abspath(path.dirname(__file__))
        with sqlite3.connect(
            self.基础路径 + "/数据库.sqlite", check_same_thread=False
        ) as self.数据库连接:
            self.数据库句柄 = self.数据库连接.cursor()
            self.数据库句柄.execute(
                """CREATE TABLE IF NOT EXISTS 生成记录 (
                    谓语 TEXT,
                    宾语 TEXT,
                    生成次数 INTEGER DEFAULT 1
                    );"""
            )

    def 写入数据库(self, 谓语: str = "", 宾语: str = "") -> None:
        # 生成次数 ++
        self.数据库句柄.execute(
            """SELECT 生成次数 FROM 生成记录
                WHERE 谓语=? AND 宾语=?""",
            (谓语, 宾语),
        )
        生成次数 = self.数据库句柄.fetchall()
        if len(生成次数):
            更新生成次数 = 生成次数[0][0] + 1
            self.数据库句柄.execute(
                """UPDATE 生成记录
                    SET 生成次数 =?
                    WHERE 谓语=? AND 宾语=?""",
                (更新生成次数, 谓语, 宾语),
            )
        else:
            self.数据库句柄.execute(
                """INSERT INTO 生成记录(谓语, 宾语, 生成次数)
                    VALUES(?,?,?)""",
                (谓语, 宾语, 1),
            )
        self.数据库连接.commit()

    def 读取数据库(self) -> list:
        # 生成记录按照生成次数排序
        self.数据库句柄.execute(
            """SELECT * FROM 生成记录
                ORDER BY 生成次数 DESC"""
        )
        生成记录 = self.数据库句柄.fetchall()
        return 生成记录


# 命令行界面
if __name__ == "__main__":
    生成器: 生成器类 = 生成器类()
    print("欢迎使用小嘿作文生成器！按 Ctrl+C 退出。")
    print("主题词示例：")
    print(", ".join([示例[0] + "|" + 示例[1] for 示例 in 生成器.主题词示例]))
    while True:
        print()
        谓语 = input("请输入主题谓语: ")
        宾语 = input("请输入主题宾语: ")
        作文: 作文类 = 生成器.生成作文(谓语, 宾语)
        print(作文.谓语 + 作文.宾语)
        for 段落 in 作文.文章:
            print(段落)
        print(f"（共 {作文.段数} 段，{作文.字数} 字）")
