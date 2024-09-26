## sql注入

这两天adworld不知道为啥都打不了，就bbuoj上随便找题做了

![image-20240725233821817](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240725233821817.png)

首先盲注看是否有过滤

![image-20240725233637051](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240725233637051.png)



可以看到完全没有过滤，直接用户名处注入就可以了，首先判断是几个行

![image-20240725233731908](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240725233731908.png)

结果就直接得到flag了，太低级了

如果是其他的话，在这里我们就应该对于数据库版本信息收集

之后可以查询database（），version（），user（）等查看数据库类型，用户名，版本等。

以MySQL数据库为例（比赛常见的），MySQL数据库有一个显著的特点就是information_schema数据库是MySQL自带的，它提供了访问数据库元数据的方式。

接下来我们可以通过构造sql语句，查询我们感兴趣的数据库->感兴趣的表->找出表中重要的行

- `CONCAT`函数用于将多个字符串值拼接成一个字符串。比如只有一个注入点，可以使用concat（id，user，password）一次性查询到三个数据
- `GROUP_CONCAT`函数用于将多个行的值拼接成一个字符串，例如，如果你有一个包含多个行的`names`列，`GROUP_CONCAT(names SEPARATOR ', ')`将返回所有`names`值的以逗号分隔的单个字符串。

当然弱密钥这样更简单，，，

![image-20240725233538416](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240725233538416.png)

![image-20240725233550399](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240725233550399.png)

# [NewStarCTF 公开赛赛道]So Baby RCE

这道题首先看php函数是什么，也就是个对这些的过滤然后执行命令，可以看到基本把我能用的命令都给过滤了，连亦或构造都不行

![image-20240725234223248](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240725234223248.png)

我首先的想法就是没过滤curl的话，我就直接在kali上传一个端口80给php反弹shell直接给他在服务器提取然后执行php反弹shell（思路很简单

问题是这不是打局域网靶机那样，buuoj访问不到我的地址，这给如何办，还需要想想

