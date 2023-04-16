# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request

from 生成器.生成器 import 作文类, 生成器类
from 统计 import 统计类

app = Flask(__name__, template_folder="网站模版", static_folder="网站资源", static_url_path="")
生成器: 生成器类 = 生成器类()
谷歌统计: 统计类 = 统计类()


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


def 检查输入(主题谓语: str, 主题宾语: str) -> tuple[bool, bool, bool, str]:
    """检查输入
    主页, 谓语错误, 宾语错误, 错误信息 = 检查输入(主题谓语, 主题宾语)
    if not any((主页, 谓语错误, 宾语错误)):
        作文: 作文类 = 生成器.生成作文(主题谓语=主题谓语, 主题宾语=主题宾语)
    """
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
    return 主页, 谓语错误, 宾语错误, 错误信息


@app.route("/", methods=["GET"])
def 作文生成器主页():
    # 初始化网页信息
    主题谓语: str = request.args.get("谓语", "")
    主题宾语: str = request.args.get("宾语", "")
    作文: 作文类 = 作文类()
    用户量, 访问量 = 谷歌统计.获得统计信息()
    主页, 谓语错误, 宾语错误, 错误信息 = 检查输入(主题谓语, 主题宾语)
    if not any((主页, 谓语错误, 宾语错误)):
        作文: 作文类 = 生成器.生成作文(主题谓语=主题谓语, 主题宾语=主题宾语)
    return render_template(
        "主页.html",
        主题谓语=主题谓语,
        主题宾语=主题宾语,
        文章=作文.文章,
        段数=作文.段数,
        字数=作文.字数,
        示例=生成器.示例库,
        示例数量=min(len(生成器.示例库), 20),
        主页=主页,
        谓语错误=谓语错误,
        宾语错误=宾语错误,
        错误信息=错误信息,
        用户量=用户量,
        访问量=访问量,
    )


@app.route("/事例/", methods=["GET"])
@app.route("/名言/", methods=["GET"])
def 素材生成器主页():
    # 初始化网页信息
    主题谓语: str = request.args.get("谓语", "")
    主题宾语: str = request.args.get("宾语", "")
    语料类别: str = request.path.strip("/")
    作文: 作文类 = 作文类()
    用户量, 访问量 = 谷歌统计.获得统计信息()
    主页, 谓语错误, 宾语错误, 错误信息 = 检查输入(主题谓语, 主题宾语)
    if not any((主页, 谓语错误, 宾语错误)):
        作文: 作文类 = 生成器.生成语料(主题谓语=主题谓语, 主题宾语=主题宾语, 语料类别=语料类别)
    return render_template(
        f"{语料类别}.html",
        主题谓语=主题谓语,
        主题宾语=主题宾语,
        语料类别=语料类别,
        文章=作文.文章,
        段数=作文.段数,
        字数=作文.字数,
        示例=生成器.示例库,
        示例数量=min(len(生成器.示例库), 20),
        主页=主页,
        谓语错误=谓语错误,
        宾语错误=宾语错误,
        错误信息=错误信息,
        用户量=用户量,
        访问量=访问量,
    )


# 本地测试
if __name__ == "__main__":
    app.run(use_reloader=False, debug=True)
