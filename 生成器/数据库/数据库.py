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
