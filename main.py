import socket
import time
import json5
import json
import gc
import os
from rsa_new_copy import *
from threading import Thread

server_lenth = 2048


def get_month():
    data = time.ctime(time.time()).split(" ")
    month = "01"
    if data[1] == "Jan":
        month = "01"
    elif data[1] == "Feb":
        month = "02"
    elif data[1] == "Mar":
        month = "03"
    elif data[1] == "Apr":
        month = "04"
    elif data[1] == "May":
        month = "05"
    elif data[1] == "Jun":
        month = "06"
    elif data[1] == "Jul":
        month = "07"
    elif data[1] == "Aug":
        month = "08"
    elif data[1] == "Sep":
        month = "09"
    elif data[1] == "Oct":
        month = "10"
    elif data[1] == "Nov":
        month = "11"
    elif data[1] == "Dec":
        month = "12"
    return month


def get_date():
    data = time.ctime(time.time()).split(" ")
    return "["+data[-1]+"/"+str(get_month())+"/"+data[-3]+" "+data[-2]+"]"


def msg(strs):
    print(strs)
    data = time.ctime(time.time()).split(" ")
    data2 = data[-1]+"."+str(get_month())+"."+data[-3]
    with open("./logs/"+data2+".log", "a+") as f:
        f.write(strs+"\n")


def change_str(data_):
    try:
        try:
            re: bytes = data_[:50].encode("utf-8")+"...".encode("utf-8")
        except:
            re: bytes = data_.encode("utf-8")
    except:
        try:
            re: bytes = data_[:50]+"...".encode("utf-8")
        except:
            re: bytes = data_
    return re


def write_(lenth):
    pub, pri = rsa_key(lenth)
    with open("./data/pub.pem", "wb") as f1:
        f1.write(pub)
    with open("./data/pri.pem", "wb") as f2:
        f2.write(pri)
    del pub, pri, lenth, f1, f2


def run(addr: tuple, conn: socket.socket):
    global server_lenth
    msg(get_date()+addr[0]+":"+str(addr[1])+"连接至服务器")
    while True:
        while True:
            try:
                data = conn.recv(102400)
            except:
                msg(get_date()+addr[0]+":"+str(addr[1])+"断开连接")
                conn.close()
                del conn, addr
                return
            if len(data) <= 0:
                msg(get_date()+addr[0]+":"+str(addr[1])+"断开连接")
                conn.close()
                del data, conn, addr
                return
            try:
                data2 = data.decode("gb2312")
                data3 = json5.loads(data2)

                if data3["comm"] == "enrsa":
                    msg(get_date()+addr[0]+":" +
                        str(addr[1])+"使用了enrsa指令")
                    data_ = data3["data"]
                    pub = data3["key"]
                    lenth = data3["lenth"]
                    data_2 = enrsa(data_.encode("utf-8"), pub.encode(), lenth)
                    conn.sendall(data_2)
                    msg(get_date()+"服务端返回" +
                        addr[0]+":"+str(addr[1])+"值为："+str(change_str(data_2)))
                    del data, data2, data3, data_, pub, lenth
                    break

                elif data3["comm"] == "rsa_key_server":
                    msg(get_date()+addr[0]+":" +
                        str(addr[1])+"使用了rsa_key_server指令")
                    lenth = data3["lenth"]
                    server_lenth = lenth
                    Thread(
                        target=write_, args=(lenth,)).start()
                    conn.sendall("ok".encode("gb2312"))
                    msg(get_date()+"服务端返回"+addr[0]+":"+str(addr[1])+"值为：ok")
                    del data, data2, data3, lenth
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
                        ":"+str(addr[1])+"值为："+change_str(retu2).decode())
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
                        addr[0]+":"+str(addr[1])+"值为："+change_str(data_.decode("utf-8")).decode())
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
    if not "logs" in os.listdir():
        os.mkdir("logs")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 5000))
    s.listen(102400)
    while True:
        conn, addr = s.accept()
        Thread(target=run, args=(addr, conn)).start()
