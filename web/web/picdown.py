from flask import Flask, Response
from flask import render_template
from flask import request
import os
import urllib

app = Flask(__name__)

# 定义一个秘密文件路径
SECRET_FILE = "/tmp/secret.txt"
# 打开秘密文件并读取内容
f = open(SECRET_FILE)
# 将读取的内容作为密钥
SECRET_KEY = f.read().strip()
# 删除秘密文件
os.remove(SECRET_FILE)

# 定义根路径的路由
@app.route('/')
def index():
    # 返回名为search.html的模板
    return render_template('search.html')

# 定义/page路径的路由
@app.route('/page')
def page():
    # 获取URL参数
    url = request.args.get("url")
    try:
        # 检查URL是否以"file"开头
        if not url.lower().startswith("file"):
            # 打开URL并读取内容
            res = urllib.urlopen(url)
            value = res.read()
            # 创建响应对象，设置MIME类型为二进制流
            response = Response(value, mimetype='application/octet-stream')
            # 设置响应头，指定文件名为beautiful.jpg
            response.headers['Content-Disposition'] = 'attachment; filename=beautiful.jpg'
            return response
        else:
            # 如果URL以"file"开头，返回HACK ERROR!
            value = "HACK ERROR!"
    except:
        # 捕获异常，返回SOMETHING WRONG!
        value = "SOMETHING WRONG!"
    # 返回名为search.html的模板，并传递res参数
    return render_template('search.html', res=value)

# 定义/no_one_know_the_manager路径的路由
@app.route('/no_one_know_the_manager')
def manager():
    # 获取key参数
    key = request.args.get("key")
    # 打印密钥
    print(SECRET_KEY)
    # 检查key是否等于密钥
    if key == SECRET_KEY:
        # 获取shell参数
        shell = request.args.get("shell")
        # 执行shell命令
        os.system(shell)
        res = "ok"
    else:
        res = "Wrong Key!"
    # 返回结果
    return res

# 如果是主程序，运行Flask应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
