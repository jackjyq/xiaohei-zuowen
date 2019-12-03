# -*- coding: UTF-8 -*-
import random
from os import listdir

class 生成器:
    def __init__(self, 随机种子:int=None)->None:
        random.seed(随机种子)
        self.模版 = self.读取文件("./模版库/模版.txt")
        self.语料类型大全 = self.获取语料类型()
        self.语料库 = {}
        for 语料类型 in self.语料类型大全:
            self.语料库[语料类型] = self.读取文件("./语料库/"+语料类型+".txt")

    def 读取文件(self, 文件路径:str)->list:
        数据 = []
        with open(文件路径, "r") as 文件:
            原始数据 = 文件.readlines()
            # 去掉多余的换行符
            for 行 in 原始数据:
                数据.append(行.strip())
        return 数据

    def 获取语料类型(self)->list:
        语料类型 = []
        for 文件名 in listdir("./语料库"):
            语料类型.append(文件名[:-4])
        return 语料类型

    def 语料库洗牌(self)->None:
        for 语料类型 in self.语料类型大全:
            random.shuffle(self.语料库[语料类型])

    def 应用语料(self, 段落:str, 语料计数:dict, 语料类型:str)->str:
        待替换词 = "「"+语料类型+"」"
        while 段落.find(待替换词) >= 0:
            # 若存在待替换词
            段落 = 段落.replace(
                待替换词,
                self.语料库[语料类型][语料计数[语料类型]],
                1)
            语料计数[语料类型] += 1
        return 段落

    def 初始化语料计数(self)->dict:
        语料计数 = {}
        for 语料类型 in self.语料类型大全:
            语料计数[语料类型] = 0
        return 语料计数

    def 生成作文(self, 主题谓语:str="", 主题宾语:str="")->list:
        # 随机选择模版
        模版 = self.模版
        # 随机替换语料
        初稿 = []
        self.语料库洗牌()
        语料计数 = self.初始化语料计数()
        for 段落 in 模版:
            for 语料类型 in self.语料类型大全:
                段落 = self.应用语料(段落, 语料计数, 语料类型)
            初稿.append(段落)
        # 替换主题词
        定稿 = []
        for 段落 in 初稿:
            段落 = 段落.replace("「主题谓语」", 主题谓语)
            段落 = 段落.replace("「主题宾语」", 主题宾语)
            定稿.append(段落)
        return 定稿

# 测试代码
if __name__ == "__main__":
    生成器 = 生成器()
    print(生成器.生成作文("积极", "尝试"))