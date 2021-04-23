# -*- coding: utf-8 -*-
from odoo import models, fields, api
from json import loads
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import time


ABS_PATH_TO_CHROMEDRIVER = '/my_addons/instagram/chromedriver'  #  put your abs path to chromedriver http://i.imgur.com/tCFHGn7.png
LINK = 'https://www.instagram.com/'
FIELD_PASS = '//*[@id="loginForm"]/div/div[2]/div/label/input'
FIELD_NAME_PHONE = '//*[@id="loginForm"]/div/div[1]/div/label/input'
BTN_LOGIN = '//div/span/a[1]/button'
BTN_LOGIN_FORM = '//*[@id="loginForm"]/div/div[3]/button/div'
BTN_NOT_NOW = '//*[@id="react-root"]/section/main/div/div/div/div/button'
SECOND_BTN_NOT_NOW = '/html/body/div[4]/div/div/div/div[3]/button[2]'
EXTRACT_INFO = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]'


def get_posts_data(**kw):

    email_username_login = kw['user_login']
    my_pass = kw['user_pass']
    required_username_to_search = kw['required_acc_to_find']
    qty_req_posts = int(kw['qty_posts'])
    required_link = f'https://www.instagram.com/{required_username_to_search}'



    with webdriver.Chrome(executable_path=ABS_PATH_TO_CHROMEDRIVER) as browser:
        try:
            browser.get(LINK)
            time.sleep(3)
            try:
                browser.find_element_by_xpath(BTN_LOGIN).click()
            except Exception as e:
                print(e)

            browser.implicitly_wait(5)
            browser.find_element_by_xpath(FIELD_NAME_PHONE).send_keys(email_username_login)
            browser.find_element_by_xpath(FIELD_PASS).send_keys(my_pass)
            browser.find_element_by_xpath(BTN_LOGIN_FORM).click()
            browser.find_element_by_xpath(BTN_NOT_NOW).click()
            browser.find_element_by_xpath(SECOND_BTN_NOT_NOW).click()

            browser.get(required_link)
            resp = browser.page_source
            soup = BS(resp, 'html.parser')
            scripts = soup.find_all('script')
            data_script = scripts[10]
            content = data_script.contents[0]
            data_object = content[content.find('{"config"'):-1]
            data_json = loads(data_object)
            list_posts = data_json['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                'edges']

            result = {}
            for n, post in enumerate(list_posts[:qty_req_posts]):
                result[n] = {
                    'ID': post['node']['shortcode'],
                    'url_img': post['node']['thumbnail_src']
                }

            return result

        except Exception as e:
            print(e)
        time.sleep(20)
        browser.quit()


# kw = {'user_login': 'nickolay.varvonets@gmail.com', 'user_pass': "Varvonets16", 'qty_posts': '3', 'required_acc_to_find': "varan_dimode"}
# print(get_posts_data(**kw))


class Instagram(models.Model):
    _name = 'instagram.instagram'
    _description = 'instagram.instagram'

    name = fields.Char(string="Instagram model")

    username = fields.Char(string="Name")
    user_login = fields.Char(string="User's email/phone", required=True)
    user_pass = fields.Char(string="User's password", required=True)
    qty_posts = fields.Integer(string="Number of posts", default=3)
    required_acc_to_find = fields.Char(string="Nickname to search in instagram", required=True)

    id_post = fields.Char(string="ID of post", store=True)
    img = fields.Char(string="URL img", store=True)

    # def _add_id(self):
    #     id_post.
