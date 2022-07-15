#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time : 2022/6/27 16:34
# @Author : VeraZhao
# @File : test_download.py
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.support import expected_conditions as EC

from common.readConfig import config_url
from utils.handleFiles import HandleFiles


def test_download(drivers):
    action = ActionChains(drivers)
    waitLogin = WebDriverWait(drivers, timeout=300, poll_frequency=0.5)
    wait = WebDriverWait(drivers, timeout=60, poll_frequency=0.5,
                         ignored_exceptions=[ElementNotVisibleException, NoSuchElementException,
                                             ElementNotSelectableException, ElementClickInterceptedException])

    try:
        drivers.get(config_url('testUrl', 'url'))
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, "简历管理")))
    except Exception:
        print("Need login")
        print(drivers.current_url)

    cvTab = waitLogin.until(EC.presence_of_element_located((By.LINK_TEXT, "简历管理")))
    cvTab.click()
    drivers.find_element(by=By.CSS_SELECTOR, value=".active > a").click()
    filters = drivers.find_element(by=By.CSS_SELECTOR, value="div:nth-of-type(2) > .style_nav-item__2kSDC")
    filters.click()
    time.sleep(1)
    print(filters.text)

    while True:
        for i in range(6):
            drivers.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(0.2)

        xpath = "/div[@class='style_card-content__3r9KI']/div[@class='style_card-wrap__2UElE']"
        items = drivers.find_elements(by=By.XPATH, value=f'/{xpath}')
        for i in range(len(items)):
            print('元素xpath', f'//div[{i + 1}]{xpath}')
            item = drivers.find_element(by=By.XPATH, value=f'//div[{i + 1}]{xpath}')
            action.move_to_element(item).click().perform()
            time.sleep(4)

            username = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.candidate-name')))[0]
            phone = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                               'div > div.information-content > p.contact-way-wrapper > p > span:nth-child(2) > span')))
            email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".contact-way [href]")))
            title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".info-text > .info-text")))
            pattern = re.findall(r"\d+", phone.text)

            info = '{}&{}&{}&{}'.format(username.text, "".join(pattern), email.text, title.text)
            HandleFiles.export_info(info)
            time.sleep(0.2)

            save_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[2]/div/span')))
            action.move_to_element(save_button).click().perform()
            close_button = drivers.find_element(by=By.ID, value="矩形")
            action.move_to_element(close_button).click().perform()
            time.sleep(0.1)

        try:
            next_page = drivers.find_element(by=By.CSS_SELECTOR,
                                             value=".lg-pagination.style_pagination__10Bz4 > li[title='下一页']")
            if "lg-pagination-disabled" in next_page.get_attribute("class"):
                break
            action.move_to_element(next_page).click().perform()
            time.sleep(0.2)
        except ElementClickInterceptedException:
            print("点击异常")
            break
        except NoSuchElementException:
            print('找不到元素')
            break
    time.sleep(10)

