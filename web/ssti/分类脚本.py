import os
def find_strings_with_os(info_string):
    # 使用split方法将字符串分割成单独的类项
    class_items = info_string.split(", ")
    n=-1
    # 遍历每个类项，找出包含"os"的项目并打印
    for item in class_items:
        n+=1
        if 'os' in item:
            print(item,n)

info_string=open("1.txt").read()


# 调用函数
find_strings_with_os(info_string)
