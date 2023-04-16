# 生成器

根据[相似度模型](./相似度模型/README.md)，在[素材库](./素材库/README.md)中选取适合素材，生成文章。

## 配置

可通过 `.env` 选择相似度模型。

```.env
# 在
cp .env.default .env
```

然后编辑 `.env` 文件。

## 运行

启动小嘿作文生成器命令行版

```zsh
python3.10 -m venv venv
source venv/bin/activate
pip install -r 完整依赖包.txt

python 生成器/生成器.py
```
