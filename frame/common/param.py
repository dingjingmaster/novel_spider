#!/usr/bin/env python3.6
# -*- encoding=utf8 -*-
import os


""" MySQL """
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3308
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_NOVEL_DB = 'novel'


""" 临时目录 """
TEMP_DIR = './TEMP/'


if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)


