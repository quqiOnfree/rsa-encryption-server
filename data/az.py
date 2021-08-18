from rsa_new_copy import dersa, enrsa,rsa_key
import socket,json,rsa_new_copy,json5

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",5000))

# a,b = rsa_new_copy.rsa_key(2048)
# data = {"comm":"enrsa","data":"data","key":a.decode(),"lenth":2048}
# data2 = json.dumps(data)
# print(data2)
# s.sendall(data2.encode("gb2312"))
# data3 = s.recv(102400)
# print(rsa_new_copy.dersa(data3,b,2048))

with open("./data/pub.pem","rb") as f:
    key = f.read()
s.sendall(rsa_new_copy.enrsa("data".encode(),key,2048))
print(s.recv(102400))

# data = {"comm":"rsa_key_server","lenth":2048}
# data2 = json.dumps(data)
# s.sendall(data2.encode("gb2312"))

# data = {"comm":"rsa_key_back","lenth":2048}
# data2 = json.dumps(data)
# s.sendall(data2.encode("gb2312"))
# data3 = s.recv(4096)
# data4 = json5.loads(data3.decode("gb2312"))
# print(data4)

# lenth = 2048
# pub,pri = rsa_key(lenth)
# retu = {"pub":pub.decode(),"pri":pri.decode()}
# retu2 = json.dumps(retu)