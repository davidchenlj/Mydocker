# Mydocker
环境Python+Django<br />
Python版本2.7X <br />
Django 1.8 <br />

第一版功能<br />
   目前仅支持容器的 启动、停止、删除、创建、inspect、镜像的显示.<br />

#python2.7安装 <br />
wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz <br />
./configure --enable-shared --prefix=/usr/local/python2.7/<br />
make<br />
make install<br />
echo /usr/local/python2.7/lib/ >> /etc/ld.so.conf && ldconfig<br />

#django安装使用pip <br />
/usr/local/python2.7/bin/pip install django <br />

# 修改连接Docker地址 <br />
vim control/utils/docker_api.py <br />
domain='http://10.0.2.23:4243' <br />

运行(直接浏览器就可以访问了) <br />
/usr/local/python2.7/bin/python2.7 manage.py runserver 0.0.0.0:8080 <br />
# 容器
![Aaron Swartz](https://github.com/davidchenlj/Mydocker/raw/master/img/1.png)
创建容器<br />
![Aaron Swartz](https://github.com/davidchenlj/Mydocker/raw/master/img/2.png)
容器详情<br />
![Aaron Swartz](https://github.com/davidchenlj/Mydocker/raw/master/img/3.png)
镜像<br />
![Aaron Swartz](https://github.com/davidchenlj/Mydocker/raw/master/img/4.png)


