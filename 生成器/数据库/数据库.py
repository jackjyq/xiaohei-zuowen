# -*- coding: UTF-8 -*-
import pathlib
import sys
from datetime import datetime
from typing import Optional

# 把生成器目录加入系统路径，以便该文件可被其它文件调用
生成器目录 = str(pathlib.Path(__file__).parent.parent)
if 生成器目录 not in sys.path:
    sys.path.insert(0, 生成器目录)
from pathlib import Path

from sqlalchemy import JSON, Column, DateTime, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class Sbert_base_chinese_nli_embeddings(Base):
    """
    最长 512 Token
    https://www.sbert.net/examples/applications/computing-embeddings/README.html?highlight=encode#input-sequence-length
    """

    __tablename__ = "Sbert_base_chinese_nli_embeddings"
    sentense = Column(String(length=500), primary_key=True)
    embeddings = Column(JSON, nullable=False)
    timestamp = Column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Text_embedding_ada_002_embeddings(Base):
    """
    最长大约 8191 token, 设成500以避免消耗太多 API
    https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
    """

    __tablename__ = "Text_embedding_ada_002_embeddings"
    sentense = Column(String(length=500), primary_key=True)
    embeddings = Column(JSON, nullable=False)
    timestamp = Column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class 数据库类:
    def __init__(self) -> None:
        self.数据库路径: Path = Path(__file__).parent / "数据库.sqlite"
        self.engine = create_engine(f"sqlite+pysqlite:///{self.数据库路径}", echo=False)
        self.Session = sessionmaker(self.engine)
        Base.metadata.create_all(self.engine)

    def 读取特征向量_sbert_base_chinese_nli(self, 文本) -> Optional[list[float]]:
        # return None means not present in database
        with self.Session() as session:
            if result := session.get(Sbert_base_chinese_nli_embeddings, 文本):
                return result.embeddings
        return None

    def 插入特征向量_sbert_base_chinese_nli(self, 文本: str, 向量: list[float]):
        with self.Session() as session:
            session.add(Sbert_base_chinese_nli_embeddings(sentense=文本, embeddings=向量))
            session.commit()

    def 读取特征向量_text_embedding_ada_002(self, 文本) -> Optional[list[float]]:
        # return None means not present in database
        with self.Session() as session:
            if result := session.get(Text_embedding_ada_002_embeddings, 文本):
                return result.embeddings
        return None

    def 插入特征向量_text_embedding_ada_002(self, 文本: str, 向量: list[float]):
        with self.Session() as session:
            session.add(Text_embedding_ada_002_embeddings(sentense=文本, embeddings=向量))
            session.commit()


if __name__ == "__main__":
    数据库: 数据库类 = 数据库类()
    特征向量 = 数据库.读取特征向量_text_embedding_ada_002("小嘿")
    print(type(特征向量), 特征向量)

# class 数据库类:
#     def __init__(self) -> None:
#         # 初始化数据库
#         # 谓语 宾语 生成次数
#         # 勇于 尝试 10
#         # 积极 进去 2
#         self.基础路径 = path.abspath(path.dirname(__file__))
#         with sqlite3.connect(
#             self.基础路径 + "/数据库.sqlite", check_same_thread=False
#         ) as self.数据库连接:
#             self.数据库句柄 = self.数据库连接.cursor()
#             self.数据库句柄.execute(
#                 """CREATE TABLE IF NOT EXISTS 生成记录 (
#                     谓语 TEXT,
#                     宾语 TEXT,
#                     生成次数 INTEGER DEFAULT 1
#                     );"""
#             )

#     def 写入数据库(self, 谓语: str = "", 宾语: str = "") -> None:
#         # 生成次数 ++
#         self.数据库句柄.execute(
#             """SELECT 生成次数 FROM 生成记录
#                 WHERE 谓语=? AND 宾语=?""",
#             (谓语, 宾语),
#         )
#         生成次数 = self.数据库句柄.fetchall()
#         if len(生成次数):
#             更新生成次数 = 生成次数[0][0] + 1
#             self.数据库句柄.execute(
#                 """UPDATE 生成记录
#                     SET 生成次数 =?
#                     WHERE 谓语=? AND 宾语=?""",
#                 (更新生成次数, 谓语, 宾语),
#             )
#         else:
#             self.数据库句柄.execute(
#                 """INSERT INTO 生成记录(谓语, 宾语, 生成次数)
#                     VALUES(?,?,?)""",
#                 (谓语, 宾语, 1),
#             )
#         self.数据库连接.commit()

#     def 读取数据库(self) -> list:
#         # 生成记录按照生成次数排序
#         self.数据库句柄.execute(
#             """SELECT * FROM 生成记录
#                 ORDER BY 生成次数 DESC"""
#         )
#         生成记录 = self.数据库句柄.fetchall()
#         return 生成记录
