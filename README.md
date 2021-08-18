# rsa加密服务端

#### 介绍
这个是专门解决多语言不互通的问题而建立的服务端（功能尚不完全，请等后续更新）
组织官网：[hcteam.top](https://hcteam.top/)

#### 软件架构
利用pycryptodome库进行加密、解密，
利用socket库进行网络传输，
利用multiprocessing进行多线程处理任务


#### 安装教程

1.  安装[requirements.txt](requirements.txt),cmd指令：pip install -r requirements.txt
2.  运行[main.py](main.py)就能用了

#### 使用说明

1.  服务端地址是127.0.0.1:5000，有需要可以更改
2.  如何传输加密指令？向服务端发送{"comm":"enrsa","data":string类型的数据,"key":pub,"lenth":密钥大小（一般是2048）}，这个在[a文件](./data/a)里面有，返回值是加密后的数据，类型：python中是bytes,c/c++ 貌似是unsigned char
3.  如何解密？直接向服务端发送对方加密过的数据
4.  编码方式：gb2312
5.  修改服务端的密钥：[data](./data)文件夹里面的[pub.pem](./data/pub.pem)和[pri.pem](./data/pri.pem)

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request