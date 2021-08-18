import socket
import multiprocessing
import time
import json5
import json
import gc
from rsa_new_copy import *

server_lenth = 2048


def get_month():
    data = time.ctime(time.time()).split(" ")
    month = 1
    if data[1] == "Jan":
        month = 1
    elif data[1] == "Feb":
        month = 2
    elif data[1] == "Mar":
        month = 3
    elif data[1] == "Apr":
        month = 4
    elif data[1] == "May":
        month = 5
    elif data[1] == "Jun":
        month = 6
    elif data[1] == "Jul":
        month = 7
    elif data[1] == "Aug":
        month = 8
    elif data[1] == "Sep":
        month = 9
    elif data[1] == "Oct":
        month = 10
    elif data[1] == "Nov":
        month = 11
    elif data[1] == "Dec":
        month = 12
    return month


def get_date():
    data = time.ctime(time.time()).split(" ")
    return "["+data[-1]+":"+str(get_month())+":"+data[-3]+":"+data[-2]+"]"


def msg(strs):
    print(strs)
    data = time.ctime(time.time()).split(" ")
    data2 = data[-1]+"."+str(get_month())+"."+data[-3]
    with open("./logs/"+data2+".log", "a+") as f:
        f.write(strs+"\n")


def change_str(data_: str):
    try:
        re = data_[:50]+"..."
    except:
        re = data_
    return re


def run(addr, conn):
    global server_lenth
    msg(get_date()+addr[0]+":"+str(addr[1])+"连接至服务器")
    while True:
        while True:
            data = conn.recv(102400)
            if len(data) <= 0:
                msg(get_date()+addr[0]+":"+str(addr[1])+"断开连接")
                conn.close()
                del data, conn, addr
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
                    msg(get_date()+addr[0]+":" +
                        str(addr[1])+"使用了rsa_key_server指令")
                    lenth = data3["lenth"]
                    server_lenth = lenth
                    pub, pri = rsa_key(lenth)
                    with open("./data/pub.pem", "wb") as f1:
                        f1.write(pub)
                    with open("./data/pri.pem", "wb") as f2:
                        f2.write(pri)
                    conn.sendall("ok".encode("gb2312"))
                    msg(get_date()+"服务端返回"+addr[0]+":"+str(addr[1])+"值为：ok")
                    del data, data2, data3, lenth, pub, pri, f1, f2
                    break

                elif data3["comm"] == "rsa_key_back":
                    msg(get_date()+addr[0]+":" +
                        str(addr[1])+"使用了rsa_key_back指令")
                    lenth = data3["lenth"]
                    pub, pri = rsa_key(lenth)
                    retu = {"pub": pub.decode(), "pri": pri.decode()}
                    retu2 = json.dumps(retu)
                    conn.sendall(retu2.encode("gb2312"))
                    msg(get_date()+"服务端返回"+addr[0] +
                        ":"+str(addr[1])+"值为："+change_str(retu2))
                    del data, data2, data3, lenth, pub, pri, retu, retu2
                    break
                else:
                    conn.sendall("你发送了错误的指令".encode("gb2312"))
                    msg(get_date()+"服务端返回"+addr[0] +
                        ":"+str(addr[1])+"值为：你发送了错误的指令")

            except Exception as error:
                try:
                    with open("./data/pri.pem", "rb") as f:
                        prikey = f.read()
                    data_ = dersa(data, prikey, server_lenth)
                    msg(get_date()+addr[0]+":"+str(addr[1])+"使用了解密指令")
                    conn.sendall(data_.decode("utf-8").encode("gb2312"))

                    msg(get_date()+"服务端返回" +
                        addr[0]+":"+str(addr[1])+"值为："+change_str(data_.decode("utf-8")))
                    del data, f, prikey, data_, error
                    break

                except:
                    msg(get_date()+str(error))
                    msgs = json.dumps(
                        {"error": "服务端发生错误，可能是你发送了错误的指令，也有可能是服务端本身错误，错误是：{}".format(str(error))})
                    conn.sendall(msgs.encode('gb2312'))
                    del error, data
            time.sleep(0.001)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))
    s.listen(102400)
    while True:
        conn, addr = s.accept()
        multiprocessing.Process(target=run, args=(addr, conn)).start()
