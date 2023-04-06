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
pip install -r requirements.txt

python 生成器/生成器.py
```

## 接口

除了 `rerequirements.txt`，运行 `生成器.py` 所需文件都在 `生成器/` 文件夹内。此外，`生成器` 仅提供如下接口，以供 `网站服务器.py` 调用。

```python
from 生成器.生成器 import 作文类, 生成器类

作文: 作文类 = 生成器.生成作文(主题谓语=主题谓语, 主题宾语=主题宾语)
```
