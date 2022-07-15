#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time : 2022/7/4 18:01
# @Author : VeraZhao
# @File : readConfig.py

import configparser
import os.path


def config_path():
    curPath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(curPath, "config.ini")


def config_url(key, value):
    config = configparser.ConfigParser()
    config.read(config_path(), encoding='utf-8')
    return config.get(key, value)
