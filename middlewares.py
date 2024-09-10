# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
import json

class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.driver = webdriver.Firefox(executable_path='C:/Users/18753/Selenium/geckodriver.exe')
        self.driver.set_window_size(1400, 700)
        self.driver.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.driver, self.timeout)
        with open('C:/Users/18753/Selenium/taobao.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        self.driver.get('https://www.taobao.com')
        for cookie in listCookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            self.driver.add_cookie(cookie)
        self.driver.get('https://www.taobao.com')

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        self.logger.debug('Firefox is starting...')
        page = request.meta.get('page', 1)
        try:
            self.driver.get(request.url)
            if page > 1:
                input_ = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input_.clear()
                input_.send_keys(page)
                submit.click()

            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active> span'), str(page)))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8', status=200)

        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('FIREFOX_SERVICE_ARGS'))
