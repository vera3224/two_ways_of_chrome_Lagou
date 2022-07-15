一、Remote Chrome 前置准备
---
- 将/Applications/Google Chrome 添加到环境变量$PATH, `export PATH="/Applications/Google Chrome.app/Contents/MacOS":$PATH`
- 在本机的下载目录下新建一个文件夹 download_cvs
- 新开一个terminal窗口，进入项目目录输入  `Google\ Chrome --remote-debugging-port=9223 --user-data-dir="~/ChromeProfile"` 开启Chrome 服务
- 在开启的Chrome中打开设置>高级, 将下载位置修改到下载目录下的/download_cvs，关闭 "下载前询问每个文件的保存位置"
- 在开启的Chrome中登录拉钩，切换到企业版>简历管理>初筛 第1页(最好先点开一份简历确保将页面上的指引动画都关闭),再回到简历列表
<img width="1387" alt="image" src="https://user-images.githubusercontent.com/11629849/176681633-79a8c8cb-731d-4aa7-8c2d-88dbcbab21ab.png">


环境
---
- python 3.7
- Chrome 102
- selenium 4.2.0
- 拉取代码以后,通过 `python -m venv venv` 创建名为venv的虚拟环境
- 在虚拟环境创建好后 `source venv/bin/activate` 进行激活
- 通过 `pip install -r requirements.txt` 安装package

运行
---
- 新开一个terminal窗口，进入项目目录输入  `Google\ Chrome --remote-debugging-port=9223 --user-data-dir="~/ChromeProfile"` 开启Chrome 服务
- 在激活后的虚拟环境下运行 ` pytest test_remoteChrome.py`，会继续在开启的Chrome中执行selenium代码
- 运行结束后 退出虚拟环境 `deactivate`


---

二、读取local Chrome 数据
---
- 在虚拟环境创建好后 `source venv/bin/activate` 进行激活
- 在激活后的虚拟环境下运行 `pytest test_download.py` 
- 运行结束后 退出虚拟环境 `deactivate`

