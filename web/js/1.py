#写一个md5加密
import hashlib

def md5_encrypt(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

# 测试
string = '288c273b03dd3dcfb65fc8fe8146175d29ef3ee8'+md5_encrypt('/welcome.txt')
encrypted_string = md5_encrypt(string)
print(encrypted_string)