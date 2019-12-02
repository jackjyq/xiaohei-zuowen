# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request
from 生成器算法 import 生成器

app = Flask(__name__)
生成器 = 生成器()


def 统计(作文:list)->(int, int):
    总字数 = 0
    总段数 = len(作文)
    for 段落 in 作文:
        总字数 += len(段落)
    return 总字数, 总段数


@app.route('/',methods = ['POST', 'GET'])
def 显示网页():
    主题动词 = "树立"
    主题名词 = "理想"
    作文 = ""
    总段数 = 0
    if request.method == 'POST':
        # 获取表单信息
        表单 = request.form
        主题动词 = 表单["主题动词"]
        主题名词 = 表单["主题名词"]
        # 调用生成器算法
        生成器.主题["主题动词"] = 主题动词
        生成器.主题["主题名词"] = 主题名词
        作文 = 生成器.生成作文()
        总字数, 总段数 = 统计(作文)
    return render_template(
            "index.html", 
            主题动词 = 主题动词,
            主题名词 = 主题名词,
            作文 = 作文,
            总段数 = 总段数,
            总字数 = 总字数
            )


if __name__ == '__main__':
    app.run(debug = True)