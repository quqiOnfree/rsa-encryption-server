import socket,multiprocessing,time,json5
from rsa_new_copy import *

server_lenth = 2048

def run(addr,conn):
    print(addr,"连接至服务器")
    while True:
        while True:
            data = conn.recv(102400)
            if len(data) == 0:
                break
            try:
                data2 = data.decode("gb2312")
                data3 = json5.loads(data2)
                if data3["comm"] == "enrsa":
                    data_ = data3["data"]
                    pub = data3["key"]
                    lenth = data3["lenth"]
                    conn.sendall(enrsa(data_.encode("utf-8"),pub.encode(),lenth))
                    break
            except Exception as error:
                print(error)
                with open("./data/pri.pem","rb") as f:
                    prikey = f.read()
                data_ = dersa(data,prikey,server_lenth)
                conn.sendall(data_.decode("utf-8").encode("gb2312"))
                break
            time.sleep(0.001)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("127.0.0.1",5000))
    s.listen(4096)
    while True:
        conn,addr = s.accept()
        multiprocessing.Process(target=run,args=(addr,conn)).start()
    