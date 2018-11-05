# tests valid user can login to the dashboard (uses selenium)
from django.shortcuts import get_object_or_404
from ...models import Stock, Trade, Profile, User
from ..factories import UserFactory, StockFactory, TradeFactory
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

class TestLogin(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver('/home/ben/path_executable/chromedriver')
        cls.selenium.implicitly_wait(10)
        user = UserFactory.create(username='login_user')

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
        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys(user.username)
        pass_input = self.selenium.find_element_by_id("id_password")
        pass_input.send_keys(user.password)
        self.selenium.find_element_by_name("submit").click()
        # Test dashboard shows correctly
        self.assertIn('%s%s' % (self.live_server_url, '/dash/'), self.selenium.current_url)
        stock_card = self.selenium.find_element_by_id(stock.ticker)
        card_name = stock_card.find_element_by_class_name('stock_name').text()
        self.assertIn(stock.name, card_name)
