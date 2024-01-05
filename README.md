###Final project of DBMS. ###

![1](image/requirements.png)

![2](image/er.png)

0. Prepare

```
sudo apt-get update
sudo apt-get install mysql-server
Install Conda
conda create --name mysql python=3.8
conda activate mysql
conda install pymysql
```

1. 默认没密码，得配置密码

```
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;
```

2. 创建数据库

```
CREATE DATABASE db;
```
复制sql.txt的建表语句

3. 运行

```
bash run.sh
```
若是有奇怪的框框，参考解决方案https://segmentfault.com/a/1190000022249793