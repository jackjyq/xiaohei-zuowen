# 小嘿作文生成器

根据输入的主题谓语、主题宾语，生成中学考试风格的作文。
本工具使用了 [BERT](https://huggingface.co/uer/sbert-base-chinese-nli) 模型，用以计算语料与主题词的相似度。

## 开始使用

[<img src="./资源/图片/二维码.png" width="350">](https://zuowen.jackjyq.com/)

## 效果展示

> >

莎士比亚写道：“即使被关在果壳之中，我仍自以为是无限宇宙之王。”人生在世，总会被一些东西束缚，只有勇于尝试，才能冲破障碍，向星辰大海进发。这样就要求我们勇于尝试,以此来丰富充实人生，增加其厚度。

在生命的河流中，每个人都想游得轻松，快捷，姿势优美。悠悠千年的人类历史，沉淀出了厚重的文化。勇于尝试的人是形成这种文化的骨干。

见义勇为英雄方俊明，勇于尝试，纵身一跃，却被命运撞得头破血流。在轮椅上度过青春，但你却固执地相信善良，丝毫不悔。今天你不能起身，但我们知道，你早已站立在所有人的面前。由此可见，勇于尝试方能让人生的鲜花绚丽多彩。只有勇于尝试，才能朝着目标奔跑。有了尝试，就不会在人生的道路上迷失自我。尝试是人生最重要的关键词之一。

袁隆平勇于尝试，以解决中国人的粮食问题为己任，头顶烈日，脚踩烂泥，研究杂交水稻的新品种，一次又一次的为科学作出的卓越的贡献。这足以说明，勇于尝试是帮助他登上生命巅峰的发动机。正确对待尝试，能够让我们不怕困难，披荆斩棘，攀登高峰。尝试对每个人来说都很重要。

千万捐赠的老人马旭，勇于尝试，少小离家乡音无改，曾经勇冠巾帼如今再让世人惊叹。以点滴积蓄汇成大河灌溉一世的乡愁，你毕生节俭只为一次奢侈，耐得清贫守得心灵的高贵。假如他勇于尝试，就不可能取得如此辉煌的成就。勇于尝试，才会有水滴石穿的精神，永不间断的前行。我们看重尝试，是因为它能成就我们。

滚滚长江东逝水，浪花流去时光。历史的经验启示我们：成功来自勇于尝试。

勇于尝试虽不容易，但并非无法做到。席慕蓉说：“生命是一条奔流不息的河，我们都是那个过河的人。”是的，要顺利地渡过这条河，必须勇于尝试。我们应当不忘初心，砥砺前行，才能在人生精神的天空中熠熠生辉。（共 717 字）

## 文件结构

### [生成器/](./生成器/README.md)

生成器程序、模板、素材

### 网页/

存放网站的 HTML 文件

### 资源/

存放网站的图片等文件

### 网站服务器.py

网站服务器主文件

其余未说明的文件一般为系统自动生成

## 本地运行

```zsh
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python 网站服务器.py
```

## 远程部署

假设服务器名 vultr, 可通过 `ssh vultr` 连接

### 1. 上传代码

在服务器创建仓库

```zsh
cd ~
git init zuowen.jackjyq.com
cd zuowen.jackjyq.com
git config --local receive.denyCurrentBranch updateInstead
```

在本地电脑，上传代码

```zsh
git remote add vultr vultr:~/zuowen.jackjyq.com
git push
```

在服务器安装依赖

```zsh
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 测试能否运行，测试完按 Ctrl+C 退出
python 网站服务器.py
```

### 2. 配置 gunicorn 服务

在服务器配置 gunicorn

```zsh
sudo vim /etc/systemd/system/zuowen.jackjyq.com.service
```

粘贴如下内容

```ini
[Unit]
Description=zuowen.jackjyq.com
After=network.target

[Service]
User=jack
Group=www-data
WorkingDirectory=/home/jack/zuowen.jackjyq.com
Environment="PATH=/home/jack/zuowen.jackjyq.com/venv/bin"
ExecStart=/home/jack/zuowen.jackjyq.com/venv/bin/gunicorn --workers 1 --timeout 300 --bind unix:zuowen.jackjyq.com.sock -m 007 网站服务器:app

[Install]
WantedBy=multi-user.target
```

在服务器启动服务

```zsh
sudo systemctl start zuowen.jackjyq.com
sudo systemctl enable zuowen.jackjyq.com
sudo systemctl status zuowen.jackjyq.com
```

### 3. 配置 Nginx 服务

在服务器配置 Nginx

```zsh
sudo vim /etc/nginx/conf.d/jackjyq.com.conf
```

粘贴如下内容

```conf
server {
        listen 80;
        server_name zuowen.jackjyq.com;
        location / {
                include proxy_params;
                proxy_pass http://unix:/home/jack/zuowen.jackjyq.com/zuowen.jackjyq.com.sock;
        }
}
```

在服务器启动服务

```zsh
sudo nginx -t
sudo systemctl restart nginx
```

### 4. 配置 HTTPS

在服务器运行

```zsh
sudo certbot --nginx
```

### 5. 升级部署

如代码修改，在本地运行

```zsh
git push vultr & ssh -t vultr 'sudo systemctl restart zuowen.jackjyq.com'
```

### 参考

- [How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)
- [connect() to unix:/run/gunicorn.sock failed (13: Permission denied)](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04)

## 贡献方式

您可以通过如下方式参与贡献：

- 提交 Pull Requests 或 Issues
- 通过 Github 右上角 Sponsor 支持作者
- 分享 [https://zuowen.jackjyq.com/](https://zuowen.jackjyq.com/) 到社交媒体

## 参考

- 受到 [文章生成器](https://github.com/suulnnka/BullshitGenerator) 启发

## [授权协议](./LICENSE)

- 图片图标, 版权所有 保留所有权利
- 项目代码，基于 MIT 开源许可协议发布
- 生成作文，基于 CC0 1.0 通用协议发布
