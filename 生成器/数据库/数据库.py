# -*- coding: UTF-8 -*-
import pathlib
import pickle
import sys
from datetime import datetime
from typing import Optional

# 把生成器目录加入系统路径，以便该文件可被其它文件调用
生成器目录 = str(pathlib.Path(__file__).parent.parent)
if 生成器目录 not in sys.path:
    sys.path.insert(0, 生成器目录)
from pathlib import Path

from sqlalchemy import JSON, Column, DateTime, String, create_engine, LargeBinary
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
    """OpenAI Text Embedding

    最长大约 8191 token, 设成500以避免消耗太多 API
    https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
    """

    __tablename__ = "Text_embedding_ada_002_embeddings"
    sentense = Column(String(length=500), primary_key=True)
    embeddings = Column(LargeBinary)
    timestamp = Column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class 数据库类:
    def __init__(self, database: str = "数据库.sqlite") -> None:
        self.数据库路径: Path = Path(__file__).parent / database
        self.engine = create_engine(f"sqlite+pysqlite:///{self.数据库路径}", echo=False)
        self.Session = sessionmaker(self.engine)
        Base.metadata.create_all(self.engine)

    def 读取特征向量_sbert_base_chinese_nli(self, 文本) -> Optional[list[float]]:
        # return None means not present in database
        with self.Session() as session:
            if result := session.get(Sbert_base_chinese_nli_embeddings, 文本):
                return result.embeddings  # type: ignore
        return None

    def 插入特征向量_sbert_base_chinese_nli(self, 文本: str, 向量: list[float]):
        with self.Session() as session:
            session.add(Sbert_base_chinese_nli_embeddings(sentense=文本, embeddings=向量))
            session.commit()

    def 读取特征向量_text_embedding_ada_002(self, 文本) -> Optional[list[float]]:
        """二进制向量会转换成 object"""
        # return None means not present in database
        with self.Session() as session:
            if result := session.get(Text_embedding_ada_002_embeddings, 文本):
                return pickle.loads(result.embeddings)  # type: ignore
        return None

    def 插入特征向量_text_embedding_ada_002(self, 文本: str, 向量: list[float]):
        """向量会转换成二进制保存，以节省空间"""
        with self.Session() as session:
            session.add(
                Text_embedding_ada_002_embeddings(
                    sentense=文本, embeddings=pickle.dumps(向量)
                )
            )
            session.commit()


if __name__ == "__main__":
    数据库: 数据库类 = 数据库类()
    特征向量 = 数据库.读取特征向量_text_embedding_ada_002("小嘿")
    print(type(特征向量), 特征向量)
