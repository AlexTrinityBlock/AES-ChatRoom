from util.CryptUtil import *

var1 = "abc123"
key = hash256(var1)

c_text=encrptToBase64(var1,key)

print(c_text)

print(decrptFromBase64toString(c_text,key))