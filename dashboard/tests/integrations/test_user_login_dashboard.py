# tests valid user can login to the dashboard (uses selenium)
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from django.shortcuts import get_object_or_404
from django.test.utils import override_settings
from ...models import Stock, Trade, Profile, User
from ..factories import UserFactory, StockFactory, TradeFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase, LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class TestLogin(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if 'TRAVIS' in os.environ:
            options = Options()
            options.add_argument('-headless')
            cls.selenium = Firefox(executable_path='geckodriver', options=options)
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--window-size=1420,1080')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disbale-gpu')
            chrome_options.add_argument("--disable-dev-shm-usage")
            cls.selenium = webdriver.Chrome(chrome_options=chrome_options, executable_path='/home/ben/path_executable/chromedriver')
        cls.selenium.implicitly_wait(10)
        user = UserFactory.create(username='login_user')
        user.set_password('test12345')
        user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_dashboard(self):
        user = get_object_or_404(User, username='login_user')
        stock = StockFactory.create(user_profile=user.profile)
        stock2 = StockFactory.create(user_profile=user.profile, name='testnotrades')
        # Test landing page and click login
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_id('sign_in').click()
        self.assertIn('%s%s' % (self.live_server_url, '/dash/login/'), self.selenium.current_url)
        # Test filling in form with users credentials
        self.selenium.find_element_by_id('login_username').send_keys(user.username)
        self.selenium.find_element_by_id('login_password').send_keys('test12345')
        self.selenium.find_element_by_id('login_submit').click()
        # Test dashboard shows correctly
        self.assertIn('%s%s' % (self.live_server_url, '/dash/'), self.selenium.current_url)
        stock_card = self.selenium.find_element_by_id(stock.ticker)
        card_name = stock_card.find_element_by_class_name('stock_name').text
        self.assertIn(stock.name, card_name)
