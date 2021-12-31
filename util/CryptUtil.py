from ctypes import POINTER
import hashlib
from Crypto.Cipher import AES
import base64
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

def encrptToBase64GCM(plaintextString:str, key):
    header =b"Good Samaritan"
    plaintextBytes = bytes(plaintextString, 'utf-8')
    cipher = AES.new(key, AES.MODE_GCM)
    cipher.update(header)
    cipherBytes,tag=cipher.encrypt_and_digest(plaintextBytes)
    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    json_v = [ b64encode(x).decode('utf-8') for x in [cipher.nonce, header, cipherBytes, tag ]]
    result = json.dumps(dict(zip(json_k, json_v)))
    return bytesToBase64String(bytes(result,"utf-8"))

def decrptFromBase64toStringGCM(ciphertextBase64:bytes, key):
    ciphertextBytes=Base64StringToBytes(ciphertextBase64)
    cipherGCMInfoJSON=ciphertextBytes.decode("utf-8")

    b64 = json.loads(cipherGCMInfoJSON)
    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    jv = {k:b64decode(b64[k]) for k in json_k}
    cipher = AES.new(key, AES.MODE_GCM, nonce=jv['nonce'])
    cipher.update(jv['header'])
    plaintext:bytes = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
    return plaintext.decode("utf-8")

def encrptToBase64CCM(plaintextString:str, key):
    header =b"Good Samaritan"
    plaintextBytes = bytes(plaintextString, 'utf-8')
    cipher = AES.new(key, AES.MODE_CCM)
    cipher.update(header)
    cipherBytes,tag=cipher.encrypt_and_digest(plaintextBytes)
    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    json_v = [ b64encode(x).decode('utf-8') for x in [cipher.nonce, header, cipherBytes, tag ]]
    result = json.dumps(dict(zip(json_k, json_v)))
    return bytesToBase64String(bytes(result,"utf-8"))

def decrptFromBase64toStringCCM(ciphertextBase64:bytes, key):
    ciphertextBytes=Base64StringToBytes(ciphertextBase64)
    cipherGCMInfoJSON=ciphertextBytes.decode("utf-8")

    b64 = json.loads(cipherGCMInfoJSON)
    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    jv = {k:b64decode(b64[k]) for k in json_k}
    cipher = AES.new(key, AES.MODE_CCM, nonce=jv['nonce'])
    cipher.update(jv['header'])
    plaintext:bytes = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
    return plaintext.decode("utf-8")

def AESEncrypt(plainTextString:str, key:bytes,mode="GCM"):
    if mode=="CCM":
        return encrptToBase64CCM(plainTextString,key)
    else:
        return encrptToBase64GCM(plainTextString, key)

def AESDecrypt(cipherTextString:str, key:bytes,mode="GCM"):
    if mode=="CCM":
        return decrptFromBase64toStringCCM(cipherTextString, key)
    else:
        return decrptFromBase64toStringGCM(cipherTextString, key)