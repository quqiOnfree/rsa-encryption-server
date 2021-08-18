import socket
import multiprocessing
import time
import json5
import json
import gc
from rsa_new_copy import *

server_lenth = 2048


def run(addr, conn):
    global server_lenth
    print(addr, "连接至服务器")
    while True:
        while True:
            data = conn.recv(102400)
            if len(data) <= 0:
                print(addr, "断开连接")
                return
            try:
                data2 = data.decode("gb2312")
                data3 = json5.loads(data2)

                if data3["comm"] == "enrsa":
                    data_ = data3["data"]
                    pub = data3["key"]
                    lenth = data3["lenth"]
                    conn.sendall(
                        enrsa(data_.encode("utf-8"), pub.encode(), lenth))
                    del data, data2, data3, data_, pub, lenth
                    break

                elif data3["comm"] == "rsa_key_server":
                    print(addr, "使用了rsa_key_server指令")
                    lenth = data3["lenth"]
                    server_lenth = lenth
                    pub, pri = rsa_key(lenth)
                    with open("./data/pub.pem", "wb") as f1:
                        f1.write(pub)
                    with open("./data/pri.pem", "wb") as f2:
                        f2.write(pri)
                    conn.sendall("ok".encode("gb2312"))
                    print("服务端返回", addr, "值为", "ok")
                    del data, data2, data3, lenth, pub, pri, f1, f2
                    break

                elif data3["comm"] == "rsa_key_back":
                    print(addr, "使用了rsa_key_back指令")
                    lenth = data3["lenth"]
                    pub, pri = rsa_key(lenth)
                    retu = {"pub": pub.decode(), "pri": pri.decode()}
                    retu2 = json.dumps(retu)
                    conn.sendall(retu2.encode("gb2312"))
                    print("服务端返回", addr, "值为", retu2)
                    del data, data2, data3, lenth, pub, pri, retu, retu2
                    break

            except Exception as error:
                try:
                    with open("./data/pri.pem", "rb") as f:
                        prikey = f.read()
                    data_ = dersa(data, prikey, server_lenth)
                    print(addr, "使用了解密指令")
                    conn.sendall(data_.decode("utf-8").encode("gb2312"))
                    print("服务端返回", addr, "值为", data_.decode("utf-8"))
                    del f, prikey, data_
                    break

                except:
                    print(error)
            time.sleep(0.001)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))
    s.listen(102400)
    while True:
        conn, addr = s.accept()
        multiprocessing.Process(target=run, args=(addr, conn)).start()
