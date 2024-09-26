# inget

# ![image-20240805232604763](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240805232604763.png)

说实话这道题最开始让我从id去get，我首先就是想到去爆破目录

然后是之前ssti，或者文件泄露，但是都没有

然后想到id的传参可能直接到数据库，有数据库注入，但是使用`'`',`sleep(5)`的时间盲注都没有效果

偷看了一下wp，还真是sql注入，直接构造出

```
' or 1=1 -- '
```

得到答案



### backup

首先界面是一个很简单的让我爆破目录

![image-20240805233812910](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240805233812910.png)

首先wget一下php文件看看有什么吧，得到没啥有用信息

就直接gobuster爆破吧，可以-x加一个php，index进行增加索引

爆破到一个bak的目录，`index.php.bak`懒得解压，直接wget

![image-20240805234217990](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240805234217990.png)

![image-20240805234202006](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240805234202006.png)