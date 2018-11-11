# tests valid user can login to the dashboard (uses selenium)
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from django.shortcuts import get_object_or_404
from django.test.utils import override_settings
from ...models import Stock, Trade, Profile, User
from ..factories import UserFactory, StockFactory, TradeFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase, LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

desired_cap = {
    'platform': "Mac OS X 10.12",
    'browserName': "chrome",
    'version': "latest",
}
username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']

class TestLogin(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if 'TRAVIS' in os.environ:
            cls.selenium = webdriver.Remote(command_executor='https://{}:{}@ondemand.saucelabs.com/wd/hub'.format(username, access_key), desired_capabilities=desired_cap)
        else:
            cls.selenium = WebDriver('/home/ben/path_executable/chromedriver')
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
