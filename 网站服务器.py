# -*- coding: UTF-8 -*-
import os
from typing import Union

from flask import Flask, render_template, request

from 生成器.生成器 import 作文类, 生成器类

app = Flask(__name__, template_folder="网页", static_folder="资源", static_url_path="")
生成器: 生成器类 = 生成器类()


def 全是汉字(字符串: str) -> bool:
    """检查字符串是否全是汉字

    全是汉字返回 True
    存在非汉字返回 False
    空字符串 也返回 True
    参考: https://cloud.tencent.com/developer/article/1499958
    """
    for 字符 in 字符串:
        if not "\u4e00" <= 字符 <= "\u9fa5":
            return False
    return True


@app.route("/", methods=["GET"])
def 显示网页():
    # 初始化网页信息
    主题谓语: str = request.args.get("谓语", "")
    主题宾语: str = request.args.get("宾语", "")
    作文: 作文类 = 作文类()
    主页: bool = False
    谓语错误: bool = False
    宾语错误: bool = False
    错误信息: str = ""

    if len(主题谓语) == 0 and len(主题宾语) == 0:
        主页 = True
    elif len(主题谓语) == 0:
        谓语错误 = True
        错误信息 = "请填写主题谓语"
    elif not 全是汉字(主题谓语):
        谓语错误 = True
        错误信息 = "主题谓语只能包含汉字"
    elif len(主题谓语) > 14:
        谓语错误 = True
        错误信息 = "主题谓语应少于 14 字"
    elif len(主题宾语) == 0:
        宾语错误 = True
        错误信息 = "请填写主题宾语"
    elif not 全是汉字(主题宾语):
        宾语错误 = True
        错误信息 = "主题宾语只能包含汉字"
    elif len(主题宾语) > 14:
        宾语错误 = True
        错误信息 = "主题宾语应少于 14 字"
    else:
        作文: 作文类 = 生成器.生成作文(主题谓语=主题谓语, 主题宾语=主题宾语)
    return render_template(
        "主页.html",
        主题谓语=主题谓语,
        主题宾语=主题宾语,
        文章=作文.文章,
        段数=作文.段数,
        字数=作文.字数,
        示例=生成器.主题词示例,
        示例数量=min(len(生成器.主题词示例), 20),
        主页=主页,
        谓语错误=谓语错误,
        宾语错误=宾语错误,
        错误信息=错误信息,
    )


# 本地测试
if __name__ == "__main__":
    # app.run(host="192.168.1.14", debug=True)
    app.run(use_reloader=False, debug=True)
