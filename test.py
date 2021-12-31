from util.CryptUtil import *

var1 = b"abc123"

base64_bytes = base64.b64encode(var1)
base64_message = base64_bytes.decode('ascii')

print(base64_message)

base64_bytes = base64_message.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
message = message_bytes.decode('ascii')

print(message)