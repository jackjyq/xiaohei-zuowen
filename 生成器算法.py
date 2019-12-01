# -*- coding: UTF-8 -*-
import random

class 生成器:
    def __init__(self)->None:
        # 初始化变量
        random.seed()
        self.模版 = {}
        self.语料库 = {}
        self.主题 = {
            "主题动词": "树立",
            "主题名词": "理想",
            "主题类型": "道德型"
        }
        # 读取相应文件
        self.模版["一型"] = self.读取文件("./模版/一型.txt")
        self.语料库["名人名言"] = self.读取文件("./语料库/名人名言.txt")
        self.语料库["道德型正例"] = self.读取文件("./语料库/道德型正例.txt")
        self.语料库["道德型反例"] = self.读取文件("./语料库/道德型反例.txt")

    def 读取文件(self, 文件路径:str)->list:
        数据 = []
        with open(文件路径, "r") as 文件:
            原始数据 = 文件.readlines()
            # 去掉多余的换行符
            for 行 in 原始数据:
                数据.append(行.strip())
        return 数据

    def 语料库洗牌(self):
        random.shuffle(self.语料库["名人名言"])
        random.shuffle(self.语料库["道德型正例"])
        random.shuffle(self.语料库["道德型反例"])

    def 应用语料(self, 段落:str, 语料计数:dict, 语料类型:str)->str:
        待替换词 = "「" + 语料类型 +"」"
        语料库类型 = 语料类型
        if 语料库类型 != "名人名言":
            语料库类型 = self.主题["主题类型"] + 语料类型
        while 段落.find(待替换词) >= 0:
            # 若存在待替换词
            段落 = 段落.replace(
                待替换词,
                self.语料库[语料库类型][语料计数[语料类型]],
                1)
            语料计数[语料类型] += 1
        return 段落

    def 生成作文(self, 模版类型:str="一型")->list:
        作文 = []
        模版 = self.模版[模版类型]
        # 洗牌和语料计数可防止重复选取同一条语料
        self.语料库洗牌()
        语料计数 = {
            "名人名言": 0,
            "正例": 0,
            "反例": 0
        }
        for 段落 in 模版:
            段落 = self.应用语料(段落, 语料计数, "名人名言")
            段落 = self.应用语料(段落, 语料计数, "正例")
            段落 = self.应用语料(段落, 语料计数, "反例")
            段落 = 段落.replace("「主题动词」", self.主题["主题动词"])
            段落 = 段落.replace("「主题名词」", self.主题["主题名词"])
            作文.append(段落)
        return 作文