# -*- coding: UTF-8 -*-
import random, sqlite3
from os import listdir


class 生成器:
    def __init__(self, 随机种子: int = None) -> None:
        random.seed(随机种子)
        self.模版库 = {}
        self.模版列表 = self.获取列表("./模版库")
        for 模版名称 in self.模版列表:
            self.模版库[模版名称] = self.读取文件("./模版库/" + 模版名称 + ".txt")
        self.语料列表 = self.获取列表("./语料库")
        self.语料库 = {}
        for 语料名称 in self.语料列表:
            self.语料库[语料名称] = self.读取文件("./语料库/" + 语料名称 + ".txt")
        self.作文总数 = self.计算作文总数()
        self.数据库 = 数据库()

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
            语料名称.append(文件名[:-4])
        return 语料名称

    def 语料库洗牌(self) -> None:
        for 语料名称 in self.语料列表:
            random.shuffle(self.语料库[语料名称])

    def 应用语料(self, 段落: str, 语料计数: dict, 语料名称: str) -> str:
        待替换词 = "「" + 语料名称 + "」"
        while 段落.find(待替换词) >= 0:
            # 若存在待替换词
            段落 = 段落.replace(待替换词, self.语料库[语料名称][语料计数[语料名称]], 1)
            语料计数[语料名称] += 1
        return 段落

    def 初始化语料计数(self) -> dict:
        语料计数 = {}
        for 语料名称 in self.语料列表:
            语料计数[语料名称] = 0
        return 语料计数

    def 生成作文(self, 主题谓语: str = "", 主题宾语: str = "") -> list:
        # 随机选择模版
        模版 = random.choice(list(self.模版库.values()))
        # 随机替换语料
        初稿 = []
        self.语料库洗牌()
        语料计数 = self.初始化语料计数()
        for 段落 in 模版:
            for 语料名称 in self.语料列表:
                段落 = self.应用语料(段落, 语料计数, 语料名称)
            初稿.append(段落)
        # 替换主题词
        定稿 = []
        for 段落 in 初稿:
            段落 = 段落.replace("「主题谓语」", 主题谓语)
            段落 = 段落.replace("「主题宾语」", 主题宾语)
            定稿.append(段落)
        # 记录数据库
        self.数据库.写入数据库(谓语=主题谓语, 宾语=主题宾语)
        return 定稿

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


class 数据库:
    def __init__(self) -> None:
        # 初始化数据库
        # 谓语 宾语 生成次数
        # 勇于 尝试 10
        # 积极 进去 2
        with sqlite3.connect("数据库.sqlite", check_same_thread=False) as self.数据库连接:
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

    def 生成作文(self, 主题谓语: str = "", 主题宾语: str = "", 模版名称: str = "经典议论文") -> list:
        # 随机选择模版
        模版 = self.模版库[模版名称]
        # 模版 = random.choice(list(self.模版库.values()))
        # 随机替换语料
        初稿 = []
        self.语料库洗牌()
        语料计数 = self.初始化语料计数()
        for 段落 in 模版:
            for 语料名称 in self.语料列表:
                段落 = self.应用语料(段落, 语料计数, 语料名称)
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
    print("欢迎使用小嘿作文生成器！按 Ctrl+C 退出。")
    while True:
        谓语 = input("请输入主题谓语:")
        宾语 = input("请输入主题宾语:")
        作文 = 生成器.生成作文("积极", "尝试")
        for 段落 in 作文:
            print(段落)
