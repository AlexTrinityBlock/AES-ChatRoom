from util.CryptUtil import *

var1 = "abc123"
key = hash256(var1)

c_text=AESEncrypt(var1,key,"CCM")

print(c_text)

print(AESDecrypt(c_text,key,"CCM"))