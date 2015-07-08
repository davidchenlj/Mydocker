# Mydocker
搭建Python+Django环境即可<br />
Python版本2.7X <br />
Django 1.8 <br />

python2.7下载地址 <br />
wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz <br />

django安装使用pip <br />
pip install django <br />

# 修改连接Docker地址 <br />
# vim control/utils/docker_api.py <br />
domain='http://10.0.2.23:4243' <br />


运行(直接浏览器就可以访问了) <br />
python2.7 manage.py runserver 0.0.0.0:8080 <br />


