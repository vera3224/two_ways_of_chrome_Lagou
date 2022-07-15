#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time : 2022/6/21 13:32
# @Author : VeraZhao
# @File : test_remoteChrome.py
import re
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.support import expected_conditions as EC

from utils.handleFiles import HandleFiles


def test_remoteChrome():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    print(options.to_capabilities())
    action = ActionChains(driver)
    wait = WebDriverWait(driver, timeout=10, poll_frequency=0.5,
                         ignored_exceptions=[ElementNotVisibleException, NoSuchElementException,
                                             ElementNotSelectableException, ElementClickInterceptedException])

    driver.refresh()
    driver.find_element(by=By.LINK_TEXT, value="简历管理").click()
    driver.find_element(by=By.CSS_SELECTOR, value=".active > a").click()
    filters = driver.find_element(by=By.CSS_SELECTOR, value="div:nth-of-type(2) > .style_nav-item__2kSDC")
    filters.click()
    time.sleep(1)
    print(filters.text)

    while True:
        for i in range(6):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(0.2)

        xpath = "/div[@class='style_card-content__3r9KI']/div[@class='style_card-wrap__2UElE']"
        items = driver.find_elements(by=By.XPATH, value=f'/{xpath}')
        for i in range(len(items)):
            print('元素xpath', f'//div[{i + 1}]{xpath}')
            item = driver.find_element(by=By.XPATH, value=f'//div[{i + 1}]{xpath}')
            action.move_to_element(item).click().perform()
            time.sleep(4)

            username = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.candidate-name')))[0]
            phone = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                               'div > div.information-content > p.contact-way-wrapper > p > span:nth-child(2) > span')))
            email = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".contact-way [href]")))
            title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".info-text > .info-text")))
            pattern = re.findall(r"\d+", phone.text)

            info = '{}-{}-{}-{}'.format(username.text, "".join(pattern), email.text, title.text)
            HandleFiles.export_info(info)
            time.sleep(0.2)

            save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[2]/div/span')))
            action.move_to_element(save_button).click().perform()
            close_button = driver.find_element(by=By.ID, value="矩形")
            action.move_to_element(close_button).click().perform()
            time.sleep(0.1)

        try:
            next_page = driver.find_element(by=By.CSS_SELECTOR,
                                            value=".lg-pagination.style_pagination__10Bz4 > li[title='下一页']")
            if "lg-pagination-disabled" in next_page.get_attribute("class"):
                break
            action.move_to_element(next_page).click().perform()
        except ElementClickInterceptedException:
            print("点击异常")
            break
        except NoSuchElementException:
            print('找不到元素')
            break
