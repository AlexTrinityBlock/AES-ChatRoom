import hashlib
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
from Crypto.Util import Counter
import json
from base64 import b64encode
from base64 import b64decode

def hash256(KeyStr: str):
    byteString = bytes(KeyStr, "utf-8")
    hashObj = hashlib.sha256()
    hashObj.update(byteString)
    return hashObj.digest()

def bytesToBase64String(byteString):
    base64_bytes = base64.b64encode(byteString)
    return base64_bytes.decode('utf-8')

def Base64StringToBytes(base64String):
    base64_bytes = base64String.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes

# def encrptToBase64(plaintextString:str, key):
#     plaintextBytes = bytes(plaintextString, 'utf-8')
#     cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
#     cipherBytes=cipher.encrypt(plaintextBytes)
#     return bytesToBase64String(cipherBytes)

def encrptToBase64(plaintextString:str, key):
    header =b"Good Samaritan"
    plaintextBytes = bytes(plaintextString, 'utf-8')
    cipher = AES.new(key, AES.MODE_GCM)
    cipher.update(header)
    cipherBytes,tag=cipher.encrypt_and_digest(plaintextBytes)
    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    json_v = [ b64encode(x).decode('utf-8') for x in [cipher.nonce, header, cipherBytes, tag ]]
    result = json.dumps(dict(zip(json_k, json_v)))
    return bytesToBase64String(bytes(result,"utf-8"))


# def decrptFromBase64toString(ciphertextBase64, key):
#     ciphertextBytes=Base64StringToBytes(ciphertextBase64)
#     cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
#     plainBytes:bytes= cipher.decrypt(ciphertextBytes)
#     return plainBytes.decode('utf-8')

def decrptFromBase64toString(ciphertextBase64:bytes, key):
    ciphertextBytes=Base64StringToBytes(ciphertextBase64)
    cipherGCMInfoJSON=ciphertextBytes.decode("utf-8")

    b64 = json.loads(cipherGCMInfoJSON)
    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    jv = {k:b64decode(b64[k]) for k in json_k}
    cipher = AES.new(key, AES.MODE_GCM, nonce=jv['nonce'])
    cipher.update(jv['header'])
    plaintext:bytes = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
    return plaintext.decode("utf-8")