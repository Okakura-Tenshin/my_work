#!/usr/bin/env python
# encoding=utf-8

from flask import Flask, request
import socket
import hashlib
import urllib
import sys
import os
import json

# 设置默认编码为latin1
reload(sys)
sys.setdefaultencoding('latin1')

app = Flask(__name__)
secret_key = os.urandom(16)

class Task:
    def __init__(self, action, param, sign, ip):
        self.action = action
        self.param = param
        self.sign = sign
        self.sandbox = md5(ip)
        if not os.path.exists(self.sandbox):
            # 为Remote_Addr创建沙盒
            os.mkdir(self.sandbox)

    def Exec(self):
        result = {'code': 500}
        if self.checkSign():
            if "scan" in self.action:
                with open(f"./{self.sandbox}/result.txt", 'w') as tmpfile:
                    resp = scan(self.param)
                    if resp == "Connection Timeout":
                        result['data'] = resp
                    else:
                        print(resp)
                        tmpfile.write(resp)
                    result['code'] = 200
            elif "read" in self.action:
                with open(f"./{self.sandbox}/result.txt", 'r') as f:
                    result['code'] = 200
                    result['data'] = f.read()
        else:
            result['msg'] = "Sign Error"
        return result

    def checkSign(self):
        return getSign(self.action, self.param) == self.sign

# 为扫描操作生成签名
@app.route("/geneSign", methods=['GET', 'POST'])
def geneSign():
    param = urllib.unquote(request.args.get("param", ""))
    action = "scan"
    return getSign(action, param)

@app.route('/De1ta', methods=['GET', 'POST'])
def challenge():
    action = urllib.unquote(request.cookies.get("action"))
    param = urllib.unquote(request.args.get("param", ""))
    sign = urllib.unquote(request.cookies.get("sign"))
    ip = request.remote_addr
    if waf(param):
        return "No Hacker!!!!"
    task = Task(action, param, sign, ip)
    return json.dumps(task.Exec())

@app.route('/')
def index():
    return open("code.txt", "r").read()

def scan(param):
    socket.setdefaulttimeout(1)
    try:
        return urllib.urlopen(param).read()[:50]
    except:
        return "Connection Timeout"

def getSign(action, param):
    return hashlib.md5(secret_key + param + action).hexdigest()

def md5(content):
    return hashlib.md5(content).hexdigest()

def waf(param):
    check = param.strip().lower()
    return check.startswith("gopher") or check.startswith("file")

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=80)
