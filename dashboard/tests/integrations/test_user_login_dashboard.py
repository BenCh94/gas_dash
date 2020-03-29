# tests valid user can login to the dashboard (uses selenium)
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from django.shortcuts import get_object_or_404
from django.test.utils import override_settings
from ...models import Stock, Trade, Profile
from django.contrib.auth.models import User
from ..factories import UserFactory, StockFactory, TradeFactory, PortfolioFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase, LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class TestLogin(LiveServerTestCase):
    fixtures = ['dashboard/fixtures/users.json', 'dashboard/fixtures/initial_data.json']
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disbale-gpu')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        if 'TRAVIS' in os.environ:
            cls.selenium = webdriver.Chrome(chrome_options=chrome_options)
        else:
            cls.selenium = webdriver.Chrome(chrome_options=chrome_options, executable_path=os.environ.get('LOCAL_CHROME'))
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.stop_client()
        cls.selenium.quit()
        super().tearDownClass()

    @override_settings(DEBUG=True)
    def test_login_dashboard(self):
        user = get_object_or_404(User, username='rootadminbc')
        stocks = Stock.objects.filter(user_profile=user.profile, status='a')
        # Test landing page and click login
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_id('sign_in').click()
        self.assertIn('%s%s' % (self.live_server_url, '/dash/login/'), self.selenium.current_url)
        WebDriverWait(self.selenium, 10000).until(EC.element_to_be_clickable((By.ID, 'login_submit')))
        # Test filling in form with users credentials
        self.selenium.execute_script(f"document.getElementById('login_username').value='{user.username}'")
        self.selenium.execute_script(f"document.getElementById('login_password').value='{os.environ.get('test_password')}'")
        self.selenium.execute_script("document.getElementById('login_submit').click()")
        # Test dashboard shows correctly
        self.assertNotIn('%s%s' % (self.live_server_url, '/dash/login/?next=/dash/'), self.selenium.current_url)
        stock_card = self.selenium.find_element_by_id(stocks.first().ticker)
        card_name = stock_card.find_element_by_class_name('stock_name').text
        self.assertIn(stocks.first().name, card_name)
        self.selenium.close()
