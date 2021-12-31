import hashlib
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
from Crypto.Util import Counter

def hash256(KeyStr: str):
    byteString = bytes(KeyStr, "utf-8")
    hashObj = hashlib.sha256()
    hashObj.update(byteString)
    return hashObj.digest()

def bytesToBase64String(byteString):
    base64_bytes = base64.b64encode(byteString)
    return base64_bytes.decode('utf-8')

def encrptToBase64(plaintextString:str, key):
    plaintextBytes = bytes(plaintextString, 'utf-8')
    cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
    cipherBytes=cipher.encrypt(plaintextBytes)
    return bytesToBase64String(cipherBytes)

