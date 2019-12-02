# -*- coding: UTF-8 -*-
from 生成器算法 import 生成器

class 命令行版生成器(生成器):
    def 输入主题(self)->None:
        self.主题["主题动词"] = input("请输入主题动词：") or "树立"
        self.主题["主题名词"] = input("请输入主题名词：") or "理想"

    def 显示作文(self)->None:
        作文 = self.生成作文()
        字数 = 0
        print()
        for 段落 in 作文:
            字数 += len(段落)
            print(段落 + "\r\n")
        print("共" + str(字数) + "字")

if __name__ == "__main__":
    生成器 = 命令行版生成器()
    生成器.输入主题()
    生成器.显示作文()