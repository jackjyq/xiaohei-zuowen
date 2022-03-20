# -*- coding: UTF-8 -*-
import os
from flask import Flask, render_template, request, send_from_directory
from 生成器算法 import 生成器
from typing import Union

app = Flask(__name__)
生成器 = 生成器()


def 统计字数(作文: list) -> Union[int, int]:
    总字数 = 0
    总段数 = len(作文)
    for 段落 in 作文:
        总字数 += len(段落)
    return 总字数, 总段数


@app.route("/", methods=["GET"])
def 显示网页():
    # 获取 URL 参数
    主题谓语 = request.args.get("谓语", "")
    主题宾语 = request.args.get("宾语", "")
    if len(主题宾语) == 0 and len(主题谓语) == 0:
        # 欢迎页
        生成记录 = 生成器.生成记录()
        return render_template("主页.html", 主题谓语="勇于", 主题宾语="尝试", 生成记录=生成记录)
    else:
        # 作文页
        作文 = 生成器.生成作文(主题谓语=主题谓语, 主题宾语=主题宾语)
        总字数, 总段数 = 统计字数(作文)
        作文[-1] += "（共" + str(总字数) + "字）"
        return render_template("作文.html", 主题谓语=主题谓语, 主题宾语=主题宾语, 作文=作文, 总段数=总段数)


# 本地测试代码
if __name__ == "__main__":
    app.run(debug=True)
