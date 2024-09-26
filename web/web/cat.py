import os, sys, getopt  # 导入操作系统、系统和命令行选项解析模块

def cat(filename, start=0, end=0) -> bytes:  # 定义cat函数，用于读取文件内容
    data = b''  # 初始化数据为空字节串
    try:
        start = int(start)  # 尝试将start参数转换为整数
        end = int(end)  # 尝试将end参数转换为整数
    except:
        start = 0  # 如果转换失败，将start设为0
        end = 0  # 将end设为0

    if filename != "" and os.access(filename, os.R_OK):  # 如果文件存在且可读
        f = open(filename, "rb")  # 打开文件以二进制模式读取
        if start >= 0:  # 如果start参数大于等于0
            f.seek(start)  # 定位到start位置
            if end >= start and end != 0:  # 如果end参数大于等于start且不等于0
                data = f.read(end - start)  # 读取从start到end之间的数据
            else:
                data = f.read()  # 读取整个文件
        else:
            data = f.read()  # 读取整个文件
        f.close()  # 关闭文件
    else:
        data = ("File `%s` not exist or can not be read" % filename).encode()  # 如果文件不存在或不可读，返回错误信息

    return data  # 返回读取的数据

if __name__ == '__main__':  # 如果该脚本作为主程序运行
    opts, args = getopt.getopt(sys.argv[1:], '-h-f:-s:-e:', ['help', 'file=', 'start=', 'end='])  # 解析命令行参数
    fileName = ""  # 初始化文件名为空字符串
    start = 0  # 初始化start为0
    end = 0  # 初始化end为0

    for opt_name, opt_value in opts:  # 遍历解析后的参数
        if opt_name == '-h' or opt_name == '--help':  # 如果参数为-h或--help
            print("[*] Help")  # 打印帮助信息
            print("-f --file File name")  # 打印文件名参数说明
            print("-s --start Start position")  # 打印起始位置参数说明
            print("-e --end End position")  # 打印结束位置参数说明
            print("[*] Example of reading /etc/passwd")  # 打印读取/etc/passwd的示例
            print("python3 cat.py -f /etc/passwd")  # 打印示例命令
            print("python3 cat.py --file /etc/passwd")  # 打印示例命令
            print("python3 cat.py -f /etc/passwd -s 1")  # 打印示例命令
            print("python3 cat.py -f /etc/passwd -e 5")  # 打印示例命令
            print("python3 cat.py -f /etc/passwd -s 1 -e 5")  # 打印示例命令
            exit()  # 退出程序

        elif opt_name == '-f' or opt_name == '--file':  # 如果参数为-f或--file
            fileName = opt_value  # 设置文件名为opt_value

        elif opt_name == '-s' or opt_name == '--start':  # 如果参数为-s或--start
            start = opt_value  # 设置start为opt_value

        elif opt_name == '-e' or opt_name == '--end':  # 如果参数为-e或--end
            end = opt_value  # 设置end为opt_value

    if fileName != "":  # 如果文件名不为空
        print(cat(fileName, start, end))  # 调用cat函数并打印结果
    else:
        print("No file to read")  # 如果文件名为空，打印提示信息
