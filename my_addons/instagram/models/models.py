# -*- coding: utf-8 -*-
from odoo import models, fields, api
from json import loads
from bs4 import BeautifulSoup as BS
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process
from selenium import webdriver
import time
import os

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot

parser = argparse.ArgumentParser(add_help=True)

class Instagram(models.Model):
    _name = 'instagram.instagram'
    _description = 'instagram.instagram'

    name = fields.Char(string="Instagram model")

    username = fields.Char(string="Name")
    user_login = fields.Char(string="User's email/phone", required=True)
    user_pass = fields.Char(string="User's password", required=True)
    qty_posts = fields.Integer(string="Number of posts", default=3)
    required_acc_to_find = fields.Char(string="Nickname to search in instagram", required=True)

    post_data = fields.Char(string="Post data", compute='_get_posts_data', tore=True)  #
    # id_post = fields.Char(string="ID of post", store=True, compute='')
    # img = fields.Char(string="URL img", store=True)


    # @api.depends('qty_posts')
    def _get_posts_data(self):

        self.post_data = 'hahaha'
        self.username = 'qqq'
        print('out')
        # with webdriver.Firefox(executable_path=ABS_PATH_TO_GECKODRIVER) as browser:

        bot = Bot()
        bot.login(username=self.user_login, password=self.user_pass)
        print('worked')

        pass

        # options = Options()
        # options.add_argument('--disable-infobars')
        # browser = webdriver.Chrome(executable_path=ABS_PATH_TO_CHROMEDRIVER, chrome_options=options, port=9515)
        # # browser = webdriver.Firefox(executable_path=ABS_PATH_TO_GECKODRIVER)
        # browser.quit()
        # print('inside')
        # executor_url = browser.command_executor._url
        # session_id = browser.session_id
        # print(session_id)
        # print(browser)



        # required_link = f'https://www.instagram.com/{self.required_acc_to_find}'
        # print(self.required_link, self.user_login)
        # print('ss')
        # browser = webdriver.Chrome(executable_path=ABS_PATH_TO_CHROMEDRIVER)
        # print(browser)
        # # with webdriver.Chrome(executable_path=ABS_PATH_TO_CHROMEDRIVER) as self.browser:
        # #     try:
        # self.browser.get(LINK)
        # print('inside', LINK)
        # self.browser.implicitly_wait(5)

                # try:
                #     self.browser.find_element_by_xpath(BTN_LOGIN).click()
                # except Exception as e:
                #     print(e)
            #
            #
            #     browser.find_element_by_xpath(FIELD_NAME_PHONE).send_keys(self.user_login)
            #     browser.find_element_by_xpath(FIELD_PASS).send_keys(self.user_pass)
            #     browser.find_element_by_xpath(BTN_LOGIN_FORM).click()
            #     browser.find_element_by_xpath(BTN_NOT_NOW).click()
            #     browser.find_element_by_xpath(SECOND_BTN_NOT_NOW).click()
            #
            #     browser.get(required_link)
            #     resp = browser.page_source
            #     soup = BS(resp, 'html.parser')
            #     scripts = soup.find_all('script')
            #     data_script = scripts[10]
            #     content = data_script.contents[0]
            #     data_object = content[content.find('{"config"'):-1]
            #     data_json = loads(data_object)
            #     list_posts = \
            #     data_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
            #         'edges']
            #
            #     result = {}
            #     for n, post in enumerate(list_posts[:self.qty_posts]):
            #         result[n] = {
            #             'ID': post['node']['shortcode'],
            #             'url_img': post['node']['thumbnail_src']
            #         }
            #
            #     return result
            #
            # except Exception as e:
            #     print(e)
        # time.sleep(10)
        # browser.quit()

# kw = {'user_login': 'nickolay.varvonets@gmail.com', 'user_pass': "Varvonets16", 'qty_posts': '3', 'required_acc_to_find': "varan_dimode"}
# x = Instagram
# print(x.get_posts_data(**kw))
