from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def rsa_key(num: int):
    key = RSA.generate(num, Random.new().read)
    return key.publickey().export_key(), key.export_key()


def enrsa(data: str, public_key: bytes, size: int):  # 加密数据，支持大文件
    lenth = int(size/1024*100)
    pubobj = PKCS1_v1_5.new(RSA.import_key(public_key))
    res = b""
    for i in range(0, len(data), lenth):
        res += pubobj.encrypt(data[i:i+lenth])
    return res


def dersa(encrypted_data: bytes, private_key: bytes, size: int):  # 解密数据，支持大文件
    lenth = int(size/1024*128)
    priobj = PKCS1_v1_5.new(RSA.import_key(private_key))
    res = b""
    for i in range(0, len(encrypted_data), lenth):
        res += priobj.decrypt(encrypted_data[i:i+lenth], "xyz")
    return res
