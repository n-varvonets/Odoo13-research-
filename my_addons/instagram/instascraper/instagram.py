from json import loads
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import time

# put here your valid data of instagram account for login
# my_username_or_phone = 'example@gmail.com'
# my_pass = "example_pass"
# required_username = "example"  # username who we are looking for http://i.imgur.com/mxX3gXo.png
# abs_path_to_chromedriver = '/home/alex/PycharmProjects/Odoo13-research-/my_addons/instagram/instascraper/chromedriver'  # absolute path to chromedriver http://i.imgur.com/BrHRsaj.png
# qty_req_posts = 3  # number of required posts

my_username_or_phone = 'nickolay.varvonets@gmail.com'
my_pass = "Varvonets16"
required_username = "varan_dimode"
abs_path_to_chromedriver = '/home/alex/PycharmProjects/Odoo13-research-/my_addons/instagram/instascraper/chromedriver'
qty_req_posts = 3

# constants
LINK = 'https://www.instagram.com/'
REQUIRED_LINK = f'https://www.instagram.com/{required_username}'
FIELD_PASS = '//*[@id="loginForm"]/div/div[2]/div/label/input'
FIELD_NAME_PHONE = '//*[@id="loginForm"]/div/div[1]/div/label/input'
BTN_LOGIN = '//div/span/a[1]/button'
BTN_LOGIN_FORM = '//*[@id="loginForm"]/div/div[3]/button/div'
BTN_NOT_NOW = '//*[@id="react-root"]/section/main/div/div/div/div/button'
SECOND_BTN_NOT_NOW = '/html/body/div[4]/div/div/div/div[3]/button[2]'
EXTRACT_INFO = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]'
QTY_POSTS = 1 + qty_req_posts


def get_list_of_posts():
    with webdriver.Chrome(executable_path=abs_path_to_chromedriver) as browser:
        try:
            browser.get(LINK)
            time.sleep(3)
            try:
                browser.find_element_by_xpath(BTN_LOGIN).click()
            except Exception as e:
                print(e)

            browser.implicitly_wait(5)
            browser.find_element_by_xpath(FIELD_NAME_PHONE).send_keys(my_username_or_phone)
            browser.find_element_by_xpath(FIELD_PASS).send_keys(my_pass)
            browser.find_element_by_xpath(BTN_LOGIN_FORM).click()
            browser.find_element_by_xpath(BTN_NOT_NOW).click()
            browser.find_element_by_xpath(SECOND_BTN_NOT_NOW).click()

            browser.get(REQUIRED_LINK)
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
            for n, post in enumerate(list_posts[:QTY_POSTS]):
                result[n] = {post['node']['shortcode']: post['node']['thumbnail_src']}

            return result

        except Exception as e:
            print(e)
        time.sleep(20)
        browser.quit()
