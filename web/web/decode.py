def encode(line, key, key2):
    return ''.join(chr(x ^ ord(line[x]) ^ ord(key[::-1][x]) ^ ord(key2[x])) for x in range(len(line)))

flag = '-M7\x10wHalc\x03"a)\x0e\x1b\x02b\x03(D\x10N\r\x17{>Ri\x02TE\x0es\x04-xEi\x14]\x17G'
print(encode(flag,'GQIS5EmzfZA1Ci8NslaoMxPXqrvFB7hYOkbg9y20W3', 'xwdFqMck1vA0pl7B8WO3DrGLma4sZ2Y6ouCPEHSQVT'))