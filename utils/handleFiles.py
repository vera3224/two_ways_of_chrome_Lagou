#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time : 2022/6/30 15:28
# @Author : VeraZhao
# @File : handleFiles.py

import os
from os import listdir

from common.readConfig import config_url

full_path = os.path.expanduser(config_url('downloadDir', 'url'))


class HandleFiles:
    def clean_file(self):
        print(full_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        for file_name in listdir(full_path):
            os.remove(full_path + file_name)
            print("Deleted" + full_path + file_name)

    def export_info(info):
        export_file = os.path.join(full_path, 'export.txt')
        with open(export_file, mode='a', encoding='utf-8') as f:
            f.write(info)
            f.write('\n')
