import requests
import time
import datetime
from requests import session
from configuration import configuration as config
from configuration import logging
from bs4 import BeautifulSoup


parser_config = config['html-parser']
host, email, password = parser_config['host'], parser_config['username'], parser_config['password']


class BookParser():

    login_url = '{}'.format(host)

    my_ebooks_url = '{}/account/my-ebooks'.format(host)
    offer_url = '{}/packt/offers/free-learning'.format(host)

    payload = {
        'op': 'Login',
        'form_id': 'packt_user_login_form',
        'email': email,
        'password': password
    }
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
        'cache-control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def __init__(self):
        self.title = ''
        self.desc = ''
        self.image = ''
        self.left_time = ''
        self.deal_html = None
        self.last_time = 0

    def parse(self):
        if not self.deal_html or self.last_time != self.get_day():

            logging.info('Parsing website')
            self.last_time = self.get_day()

            response = requests.get(self.offer_url, headers=self.headers)
            html = BeautifulSoup(response.text, 'lxml')

            self.deal_html = html.find('div', {'id': 'deal-of-the-day'})
            self.set_fields()

        self.set_left_time()

    def set_fields(self):
        self.title = self.deal_html.find(
            'div', {'class': 'dotd-title'}).text.strip()
        self.image = self.deal_html.find(
            'img', {'class': 'bookimage imagecache imagecache-dotd_main_image'}).attrs['src']
        self.desc = self.deal_html.find('div', {'class': ''}).text.strip()

    def get_day(self):
        return datetime.datetime.now().day

    def get_tomorrow(self):
        return datetime.date.today() + datetime.timedelta(days=1)

    def to_timestamp(self, date):
        return int(time.mktime(date.timetuple()))

    def set_left_time(self):
        diff = self.to_timestamp(self.get_tomorrow()) - int(time.time())
        self.left_time = time.strftime("%H:%M:%S", time.gmtime(diff))

    def get_books(self):
        with session() as c:
            response = c.post(
                self.login_url, data=self.payload, headers=self.headers)
            response = c.get(self.my_ebooks_url)
            print(c.cookies.get_dict())
            print(response.headers)
            print(response.text)
