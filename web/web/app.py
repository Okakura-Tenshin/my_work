import os  # 导入操作系统模块
import uuid  # 导入UUID模块
from flask import Flask, request, session, render_template, Markup  # 导入Flask框架的相关模块
from cat import cat  # 从cat模块导入cat函数

flag = ""  # 初始化flag变量为空字符串
app = Flask(  # 创建Flask应用实例
    __name__,  # 应用名称
    static_url_path='/',  # 静态文件URL路径
    static_folder='static'  # 静态文件目录
)
app.config['SECRET_KEY'] = str(uuid.uuid4()).replace("-", "") + "*abcdefgh"  # 设置Flask应用的SECRET_KEY

# 如果存在名为"/flag"的文件，读取其内容并删除该文件
if os.path.isfile("/flag"):
    flag = cat("/flag")
    os.remove("/flag")

@app.route('/', methods=['GET'])  # 定义根路由，处理GET请求
def index():
    detailtxt = os.listdir('./details/')  # 获取details目录下的文件列表
    cats_list = []  # 初始化一个空列表，用于存储文件名（不包含扩展名）
    for i in detailtxt:
        cats_list.append(i[:i.index('.')])  # 将文件名（不包含扩展名）添加到列表中
    return render_template("index.html", cats_list=cats_list, cat=cat)  # 渲染index.html模板，传递cats_list和cat参数

@app.route('/info', methods=["GET", "POST"])  # 定义info路由，处理GET和POST请求
def info():
    filename = "./details/" + request.args.get('file', "")  # 获取请求参数file的值，并拼接成文件路径
    start = request.args.get('start', "0")  # 获取请求参数start的值，默认为0
    end = request.args.get('end', "0")  # 获取请求参数end的值，默认为0
    name = request.args.get('file', "")[:request.args.get('file', "").index('.')]  # 获取文件名（不包含扩展名）
    return render_template("detail.html", catname=name, info=cat(filename, start, end))  # 渲染detail.html模板，传递catname和info参数

@app.route('/admin', methods=["GET"])  # 定义admin路由，处理GET请求
def admin_can_list_root():
    if session.get('admin') == 1:  # 检查session中是否存在admin键且值为1
        return flag  # 返回flag
    else:
        session['admin'] = 0  # 如果不存在，将admin键值设为0
        return "NoNoNo"  # 返回"NoNoNo"

if __name__ == '__main__':  # 如果该脚本作为主程序运行
    app.run(host='0.0.0.0', debug=False, port=5637)  # 启动Flask应用，监听所有IP地址的5637端口
