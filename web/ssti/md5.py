#写一个md5加密
import hashlib

def md5_encrypt(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

# 测试
string = '0fd3852b-7e3a-4e00-81c1-e504a1101052'+md5_encrypt('/fllllllllllllag')
encrypted_string = md5_encrypt(string)
print(encrypted_string)

