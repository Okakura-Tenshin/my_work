def encode(line, key, key2):
    # 对line进行加密，返回加密后的字符串
    return ''.join(chr(x ^ ord(line[x]) ^ ord(key[::-1][x]) ^ ord(key2[x])) for x in range(len(line)))

# app.config['flag'] = encode('', 'GQIS5EmzfZA1Ci8NslaoMxPXqrvFB7hYOkbg9y20W34', 'xwdFqMck1vA0pl7B8WO3DrGLma4sZ2Y6ouCPEHSQVT5')

def decode(line, key, key2):
    # 对line进行解密，返回解密后的字符串
    return ''.join(chr(x ^ ord(line[x]) ^ ord(key[::-1][x]) ^ ord(key2[x])) for x in range(len(line)))

# 使用示例
print(decode('-M7\x10wHalc\x03"a)\x0e\x1b\x02b\x03(D\x10N\r\x17{>Ri\x02TE\x0es\x04-xEi\x14]\x17G', 'GQIS5EmzfZA1Ci8NslaoMxPXqrvFB7hYOkbg9y20W34', 'xwdFqMck1vA0pl7B8WO3DrGLma4sZ2Y6ouCPEHSQVT5'))
