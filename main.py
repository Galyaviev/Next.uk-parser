#!/usr/bin/python
# *- coding: utf-8 -*-
from sql import *
from conf import *

from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from seleniumrequests import Firefox
from random import choice
from selenium import webdriver
import re
import datetime
import json
import requests
import time
import random

chat_id = chat_id2
number = 0
basket = 'https://www.next.co.uk/bag'
update_quantity = "https://www.next.co.uk/bag/updatequantity"
headers = {'content-type': 'application/json'}
now = datetime.datetime.now()

rany = [Keys.DOWN, Keys.UP, Keys.LEFT, Keys.RIGHT]
random.shuffle(rany)

def start():
    list = select_all()
    for date in list:
        login = date['login']
        password = date['password']
        try:
            print('Запускаю Браузер')
            options = Options()
            options.headless = False
            browser = Firefox(options=options)
            browser.delete_all_cookies()
            browser.set_window_position(0, 0)
            browser.set_window_size(1024, 1024)
            browser.get('https://www.next.co.uk/secure/account/Login')
            login_input = browser.find_element_by_id('EmailOrAccountNumber')
            ActionChains(browser).move_to_element(login_input).perform()
            paswword_input = browser.find_element_by_id('Password')
            ActionChains(browser).move_to_element(paswword_input).perform()
            paswword_input.send_keys(random.choice(rany))
            login_input.send_keys(login)
            paswword_input.send_keys(password)
            paswword_input.send_keys(random.choice(rany))
            paswword_input.send_keys(random.choice(rany))
            paswword_input.send_keys(Keys.ENTER)
            time.sleep(random.uniform(3, 5))
            soup = BeautifulSoup(browser.page_source, 'lxml')
            titleTag = soup.find('title').text
            print(titleTag)

            while titleTag == 'Access Denied':
                browser.quit()
                print('close')
                proxy_list = choice(get_proxy())
                proxy_host = proxy_list['ip']
                proxy_port = int(proxy_list['port'])
                print(proxy_host, proxy_port)
                options = Options()
                options.headless = False
                fp = webdriver.FirefoxProfile()
                fp.set_preference("browser.privatebrowsing.autostart", True)
                fp.set_preference("network.proxy.type", 1)
                fp.set_preference("network.proxy.http", proxy_host)
                fp.set_preference("network.proxy.http_port", proxy_port)
                fp.set_preference("network.proxy.https", proxy_host)
                fp.set_preference("network.proxy.https_port", proxy_port)
                fp.set_preference("network.proxy.ssl", proxy_host)
                fp.set_preference("network.proxy.ssl_port", proxy_port)
                fp.set_preference("network.proxy.ftp", proxy_host)
                fp.set_preference("network.proxy.ftp_port", proxy_port)
                fp.set_preference("network.proxy.socks", proxy_host)
                fp.set_preference("network.proxy.socks_port", proxy_port)
                fp.update_preferences()
                print('open browser')
                browser = Firefox(options=options, firefox_profile=fp)
                browser.set_window_position(0, 0)
                browser.set_window_size(1024, 648)
                browser.get('https://api.ipify.org/')
                test_ip = browser.find_element_by_tag_name('pre').text
                print(test_ip + ' ip полученное с сайта')
                print(proxy_list['ip'] + ' ip полученное с прокси')

                if test_ip == proxy_list['ip']:
                    browser.delete_all_cookies()
                    browser.get('https://www.next.co.uk/secure/account/Login')
                    login_input = browser.find_element_by_id('EmailOrAccountNumber')
                    ActionChains(browser).move_to_element(login_input).perform()
                    paswword_input = browser.find_element_by_id('Password')
                    ActionChains(browser).move_to_element(paswword_input).perform()
                    paswword_input.send_keys(random.choice(rany))
                    login_input.send_keys(login)
                    paswword_input.send_keys(password)
                    paswword_input.send_keys(random.choice(rany))
                    paswword_input.send_keys(random.choice(rany))
                    paswword_input.send_keys(Keys.ENTER)
                    time.sleep(random.uniform(3, 5))
                    soup = BeautifulSoup(browser.page_source, 'lxml')
                    titleTag = soup.find('title').text
                    print(titleTag)

            browser.get('https://www2.next.co.uk/shoppingbag')
            time.sleep(random.uniform(3, 5))
            r = browser.request('GET', basket)
            write_log(r.json())
            data = browser.request('GET', basket).json()
            coint_bug = len(data["ShoppingBag"]['Items'])
            a = coint_bug - 1

            while coint_bug >= 1:
                message = data["ShoppingBag"]['Items'][a]["StockMessage"]
                thing = data["ShoppingBag"]['Items'][a]["Description"]
                items = data["ShoppingBag"]['Items'][a]["ItemNumber"]
                size = data["ShoppingBag"]['Items'][a]["SizeDescription"]

                if "In Stock" in message:
                    coint_bug = coint_bug - 1
                    a = a - 1
                    text_telegram = 'в этом логине нашлось ' + login + ': ' + thing + ' ' + items + ' ' + size
                    web_get = tgapi+'/sendmessage?chat_id={}&text={}'.format(
                        chat_id, text_telegram)

                    requests.get(web_get)
                    print(message)

                else:
                    coint_bug = coint_bug - 1
                a = a - 1

            print(login)
            print(datetime.datetime.now())
            browser.quit()
        except Exception as e:
            with open('error.txt', 'a') as f:
                f.write(str(e) + '\n')



def get_proxy():
    url = 'http://proxy-list.org/russian/search.php?search=RU.ssl-yes&country=RU&type=any&port=any&ssl=yes'
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.set_window_position(0, 0)
    browser.set_window_size(1024, 1024)
    print('Запускаю')
    browser.get(url)
    proxy_list = browser.page_source
    regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{2,5}'
    soup = BeautifulSoup(proxy_list, 'lxml')
    table = soup.find('div', class_ = 'table').find_all('li', class_='proxy')
    lists = []

    for ip_port in table:
        ip_port = ip_port.text
        ip_port = re.findall(regexp, ip_port)
        ip_port = ip_port[0].split(':')
        proxy = {'ip':ip_port[0], 'port':ip_port[1]}
        lists.append(proxy)
    browser.quit()
    print(lists)
    return lists

def write_log(data):
    log = data
    with open('dump.json', 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)



if __name__ == '__main__':
    while number < 999999999:
        start()
