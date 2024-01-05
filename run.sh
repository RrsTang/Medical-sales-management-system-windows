#!/bin/bash

# 0. Prepare

# sudo apt-get update
# sudo apt-get install mysql-server
# Install Conda
# conda create --name mysql python=3.8
# conda activate mysql
# conda install pymysql

# 1. 默认没密码，得配置密码
# sudo mysql
# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
# FLUSH PRIVILEGES;

# 2. 创建数据库
# CREATE DATABASE db;

# 3. 运行
# 若是有奇怪的框框，参考解决方案https://segmentfault.com/a/1190000022249793

set -x
# sudo systemctl status mysql

# conda init
# conda activate mysql
export PYTHONPATH=$(pwd):$(pwd)/gui:$(pwd)/sqlhandler:$PYTHONPATH

python gui/main.py
set +x
