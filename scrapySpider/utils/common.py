#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File : common.py
@Time : 2019/04/12 09:23:58
@Author : FanZehua
@Version : 1.0
@Contact : 316679581@qq.com
@License : (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc : None
'''

# here put the import lib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def get_browser():
    chrome_option = Options()
    chrome_option.add_argument('--disable-extensions')
    chrome_option.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    browser = webdriver.Chrome(
        executable_path=r'E:\chromedriver\chromedriver_win32\chromedriver.exe',
        chrome_options=chrome_option)
    return browser
