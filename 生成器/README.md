# 生成器

生成器主文件，可单独运行，`python 生成器.py`。

## sbert_base_chinese_nli

使用 [sbert-base-chinese-nli](https://huggingface.co/uer/sbert-base-chinese-nli) 计算事例与主题词的相关性，并随机选取相关性较高的事例。这样极大增加了内存占用（100 多 MB -> 500 MB）。

## TODO：后续考虑接入 OpenAI 的 API