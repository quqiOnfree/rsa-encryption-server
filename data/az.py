from rsa_new import dersa, enrsa
import socket,json,rsa_new_copy

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("127.0.0.1",5000))
a,b = rsa_new_copy.rsa_key(2048)
data = {"comm":"enrsa","data":"data","key":a.decode(),"lenth":2048}
data2 = json.dumps(data)
print(data2)
s.sendall(data2.encode("gb2312"))
data3 = s.recv(102400)
print(rsa_new_copy.dersa(data3,b,2048))

# with open("./data/pub.pem","rb") as f:
#     key = f.read()
# s.sendall(rsa_new_copy.enrsa("data".encode(),key))
# print(s.recv(102400))