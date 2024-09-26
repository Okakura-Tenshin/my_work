import urllib.parse

decoded_str = "E5A4A7E5B885b"
encoded_str = urllib.parse.quote(decoded_str, encoding='ISO-8859-1')
print(encoded_str)
