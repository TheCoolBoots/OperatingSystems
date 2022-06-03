from base64 import b64decode
from base64 import b64encode
from hashlib import md5


# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes
# from Crypto.Util.Padding import pad, unpad


def encryptAES(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # print(iv + cipher.encrypt(pad(data, AES.block_size, 'x923')))
    # print(type(iv + cipher.encrypt(pad(data, AES.block_size, 'x923'))))
    return iv + cipher.encrypt(data)

def decryptAES(data, key, iv):
    # TODO need to store the iv from encryptAES somehow and shove it back into the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(data)


# data = b'abacdsasdfafweasdfawe'
# key = 'magic'
# hashKey = md5(key.encode('utf8')).digest()
# encrypted = encryptAES(data, hashKey)
# decrypted = decryptAES(encrypted, hashKey)
# print(type(encrypted))
# print(type(decrypted))
# print(decrypted)
