## [网鼎杯 2020 玄武组]SSRFMe

php代码审计

根据之前的学习，关注以下铭感函数

相关函数和类

file_get_contents()：将整个文件或一个url所指向的文件读入一个字符串中
readfile()：输出一个文件的内容
fsockopen()：打开一个网络连接或者一个Unix 套接字连接
curl_exec()：初始化一个新的会话，返回一个cURL句柄，供curl_setopt()，curl_exec()和curl_close() 函数使用
fopen()：打开一个文件文件或者 URL
PHP原生类SoapClient在触发反序列化时可导致SSRF



看到curl_exec就知道是ssrf了

```php
<?php
function check_inner_ip($url)
{
    $match_result=preg_match('/^(http|https|gopher|dict)?:\/\/.*(\/)?.*$/',$url);
    if (!$match_result)
    {
        die('url fomat error');
    }
    try
    {
        $url_parse=parse_url($url);
    }
    catch(Exception $e)
    {
        die('url fomat error');
        return false;
    }
    $hostname=$url_parse['host'];
    $ip=gethostbyname($hostname);
    $int_ip=ip2long($ip);
    return ip2long('127.0.0.0')>>24 == $int_ip>>24 || ip2long('10.0.0.0')>>24 == $int_ip>>24 || ip2long('172.16.0.0')>>20 == $int_ip>>20 || ip2long('192.168.0.0')>>16 == $int_ip>>16;
}

function safe_request_url($url)
{

    if (check_inner_ip($url))
    {
        echo $url.' is inner ip';
    }
    else
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        $output = curl_exec($ch);
        $result_info = curl_getinfo($ch);
        if ($result_info['redirect_url'])
        {
            safe_request_url($result_info['redirect_url']);
        }
        curl_close($ch);
        var_dump($output);
    }

}
if(isset($_GET['url'])){
    $url = $_GET['url'];
    if(!empty($url)){
        safe_request_url($url);
    }
}
else{
    highlight_file(__FILE__);
}
// Please visit hint.php locally.
?>
```

首先对于waf的限制，只允许使用http|https|gopher|dict这四个

接下来会判断是否在内网



相关协议

file协议： 在有回显的情况下，利用 file 协议可以读取任意文件的内容
dict协议：泄露安装软件版本信息，查看端口，操作内网redis服务等
gopher协议：gopher支持发出GET、POST请求。可以先截获get请求包和post请求包，再构造成符合gopher协议的请求。gopher协议是ssrf利用中一个最强大的协议(俗称万能协议)。可用于反弹shell
http/s协议：探测内网主机存活

 根据提示，可以使用四个运行的协议访问hint.php 

其中绕过内网限制，考虑构造

```
http://0.0.0.0
```

的回环绕过，但是跳转错误，不存在url

之后考虑了使用ipv6表示ipv4绕过

```
http://[0:0:0:0:0:ffff:127.0.0.1]//hint.php
```

得到hint.php

```php
 <?php
if($_SERVER['REMOTE_ADDR']==="127.0.0.1"){
  highlight_file(__FILE__);
}
if(isset($_POST['file'])){
  file_put_contents($_POST['file'],"<?php echo 'redispass is root';exit();".$_POST['file']);
}
```

观察到提示中

redispass is root

redis貌似是个软件，结合搜索引擎的搜索

首先搜索到第一个漏洞

### **Redis 未授权访问漏洞**

Redis默认情况下，会绑定`0.0.0.0:6379`，如果没有采用相关的策略，比如添加防火墙规则表面其他非信任来源IP访问等，这样会将Redis服务暴露到公网上，如果在没有设置密码认证 (一般为空)的情况下，会导致任意用户在可以访问目标服务器的情况下未授权访问Redis以及读取Redis的数据

github‘找到一个工具，但不知道怎么用

