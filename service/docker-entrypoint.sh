#!/bin/sh

# Get the user
user=$(ls /home)
chmod 740 /app/*

# 启动flask，并同时开启debug模式
# cd /app && flask --debug run -h 0.0.0.0 -p 5000

# 在无debug参数下启动flask
cd /app && flask run -h 0.0.0.0 -p 5000
