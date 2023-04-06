# 相似度模型

计算素材与用户输入的相似度，以提高生成作文的质量。

## random_similarity（默认）

随机拼凑语料，资源占用最低。

## sbert_base_chinese_nli.py

使用 [sbert-base-chinese-nli](https://huggingface.co/uer/sbert-base-chinese-nli) 模型，内存占用大约 500 MB。

## text_embedding_ada_002

使用 OpenAI 的 [text_embedding_ada_002](https://platform.openai.com/docs/guides/embeddings) 模型，需要申请 [API Key](https://platform.openai.com/account/api-keys) ，并配置到 `.env` 中。
