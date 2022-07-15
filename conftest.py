#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time : 2022/7/4 18:02
# @Author : VeraZhao
# @File : conftest.py

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from common.readConfig import config_url
from utils.handleFiles import HandleFiles

driver = None


@pytest.fixture(scope='session')
def drivers(request):
    global driver
    download_path = os.path.expanduser(config_url('downloadDir', 'url'))
    user_data = os.path.expanduser(config_url('userData', 'url'))
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument(f'--user-data-dir={user_data}')
    options.add_argument('--profile-directory=Default')
    prefs = {
        'profile.default_content_settings.popups': 0,  # 防止保存弹窗
        'download.default_directory': download_path,  # 设置默认下载路径
        "profile.default_content_setting_values.automatic_downloads": 1  # 允许多文件下载
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    if driver is None:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print(options.to_capabilities())

    def fn():
        driver.quit()

    request.addfinalizer(fn)
    return driver


@pytest.fixture(scope='session', autouse=True)
def clean_file():
    HandleFiles.clean_file(self=None)
