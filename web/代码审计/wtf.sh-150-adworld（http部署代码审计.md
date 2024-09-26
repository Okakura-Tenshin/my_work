### wtf.sh-150-adworld

![image-20240924210849919](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240924210849919.png)

相当难的一道题，以现有水平只解出一半，后面代码审计参考了wp

首先是登录页面和留言框，先爆破admin弱密钥，无结果

随便点击看到url的改变，猜测有路径泄露



尝试构造../，成功访问源代码



对代码审计，通过遍历目录 ../users/ 拿到admin的cookie，伪造登录

这里有flag相关提示

```xml
source user_functions.sh

<html>
<head>
    <link rel="stylesheet" type="text/css" href="/css/std.css">
</head>
<body>
    $ if contains 'user' ${!URL_PARAMS[@]} && file_exists "users/${URL_PARAMS['user']}" $ then
    $ local username=$(head -n 1 users/${URL_PARAMS['user']});
    $ echo "<h3>${username}'s posts:</h3>";
    $ echo "<ol>";
    $ get_users_posts "${username}" | while read -r post; do
    $ post_slug=$(awk -F/ '{print $2 "#" $3}' <<< "${post}");
    $ echo "<li><a href=\"/post.wtf?post=${post_slug}\">$(nth_line 2 "${post}" | htmlentities)</a></li>";
    $ done
    $ echo "</ol>";
    $ if is_logged_in && [[ "${COOKIES['USERNAME']}" = 'admin' ]] && [[ ${username} = 'admin' ]] $ then
    $ get_flag1
    $ fi
    $ fi
</body>
</html>

```



```
uYpiNNf/X0/0xNfqmsuoKFEtRlQDwNbS2T6LdHDRWH5p3x4bL4sxN0RMg17KJhAmTMyr8Sem++fldP0scW7g3w==
```

成功拿下一半的cookie

![image-20240924201258741](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240924201258741.png)

```
Flag: xctf{cb49256d1ab48803
```



接下来代码审计，只张贴有注入的代码

```bash
source user_functions.sh

# 创建新帖子，返回帖子ID
function create_post {
    local username=$1
    local title=$2
    local text=$3
    local hashed=$(hash_username "${username}")

    # 确保 posts 目录存在且不可列出
    mkdir posts 2> /dev/null
    touch posts/.nolist  # 不允许列出目录
    touch posts/.noread  # 不允许读取文件

    local post_id=$(basename $(mktemp --directory posts/XXXXX))
    echo ${username} > "posts/${post_id}/1"
    echo ${title} >> "posts/${post_id}/1"
    echo ${text} >> "posts/${post_id}/1"
    touch "posts/${post_id}/.nolist"
    touch "posts/${post_id}/.noread"

    # 添加到主页缓存
    echo "<li><a href=\"/post.wtf?post=${post_id}\">$(htmlentities <<< ${title})</a> by $(htmlentities <<< ${username})</li>" >> .index_cache.html

    # 添加帖子到用户的帖子缓存
    echo "${post_id}/1" >> "users_lookup/${hashed}/posts"
    echo ${post_id}
}

# 回复帖子
function reply {
    local post_id=$1
    local username=$2
    local text=$3
    local hashed=$(hash_username "${username}")

    curr_id=$(for d in posts/${post_id}/*; do basename $d; done | sort -n | tail -n 1)
    next_reply_id=$(awk '{print $1+1}' <<< "${curr_id}")
    next_file="posts/${post_id}/${next_reply_id}"

    echo "${username}" > "${next_file}"
    echo "RE: $(nth_line 2 < "posts/${post_id}/1")" >> "${next_file}"
    echo "${text}" >> "${next_file}"

    # 添加回复到用户的帖子缓存
    echo "${post_id}/${next_reply_id}" >> "users_lookup/${hashed}/posts"
}

```

reply中使用的next_file="posts/${post_id}/${next_reply_id}"会导致目录路径遍历漏洞



这个题感觉难在代码审计，使用bash搭建了http服务，

其中有执行代码的eval的函数

```bash
function include_page {
# include_page <pathname>
local pathname=$1
local cmd=""
[[ "${pathname:(-4)}" = '.wtf' ]];
local can_execute=$?;
page_include_depth=$(($page_include_depth+1))
if [[ $page_include_depth -lt $max_page_include_depth ]]
then
local line;
while read -r line; do
# check if we're in a script line or not ($ at the beginning implies script line)
# also, our extension needs to be .wtf
[[ "$" = "${line:0:1}" && ${can_execute} = 0 ]];
is_script=$?;

# execute the line.
if [[ $is_script = 0 ]]
then
cmd+=$'\n'"${line#"$"}";
else
if [[ -n $cmd ]]
then
eval "$cmd" || log "Error during execution of ${cmd}";
cmd=""
fi
echo $line
fi
done < ${pathname}
else
echo "<p>Max include depth exceeded!<p>"
fi
}
```

如果文件后缀名是.wtf，就会将名字加入变量中执行

首先名字随便构造一个，比如123

在reply界面时候，post后缀改为../users_lookup/123.wtf，123名字任意，

**此处后面还要跟%09**否则系统会默认是文件夹而不是文件，而http格式，后面的http1.1需要缩进一格跟09无间隙否则格式不正确

发送完后访问ip/users_lookup/123.wtf，可以看到直接的回显

接下来验证能否执行命令，因为在1中的flag显示了是get_flag1命令，所以我们使用拼接字符串的find命令来查找

${find,/,-iname,get_flag2}



![image-20240924204329501](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240924204329501.png)

要注意/bin这个文件是可执行命令的文件，不能直接构造cat比如${cat,/usr/bin/get_flag2}，只会输出乱码，而是应该直接去访问执行命令得到flag

![image-20240924210403450](C:\Users\10649\AppData\Roaming\Typora\typora-user-images\image-20240924210403450.png)



xctf{cb49256d1ab48803149e5ec49d3c29ca}