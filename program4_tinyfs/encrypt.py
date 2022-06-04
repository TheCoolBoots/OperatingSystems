from Crypto.Cipher import AES
from hashlib import md5
from Crypto.Random import get_random_bytes
from base64 import b64decode
from base64 import b64encode
from Crypto.Util.Padding import pad, unpad



def encryptAES(data, key:bytes, iv:bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(data)

def decryptAES(data, key:bytes, iv:bytes) -> bytes:
    # TODO need to store the iv from encryptAES somehow and shove it back into the ciphertext
    tmp = data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(tmp)



# encryptionKey = md5('asdfasdf'.encode('utf8')).digest()
# data = b'0123456789abcdef' * 10
# iv = get_random_bytes(AES.block_size)

# encrypted = encryptAES(data, encryptionKey, iv)
# decrypted = decryptAES(encrypted, encryptionKey, iv)
# print(data)
# print(len(data))
# print(encrypted)
# print(len(encrypted))
# print(decrypted)
# print(len(decrypted))
# print(data==decrypted)
