# 生成器

小嘿作文生成器命令行版，根据设计，既可被`网站服务器.py`调用，又可单独运行。

```python
python 生成器.py
```

## [素材库](./素材库/)

存储及处理素材

## [数据库](./数据库/)

数据库操作及 SQLite 存储

## [相似度模型](./相似度模型/)

计算素材与用户输入的相似度，以提高生成作文的质量。

### random_similarity

即随机指定相似度，速度最快，是最初的实现。

### sbert_base_chinese_nli.py

使用 [sbert-base-chinese-nli](https://huggingface.co/uer/sbert-base-chinese-nli) 模型，内存占用大约 500 MB。

### TODO：后续考虑接入 OpenAI 的 API
