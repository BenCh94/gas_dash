# tests valid user can login to the dashboard (uses selenium)

import unittest
from selenium import webdriver

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_signup_fire(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element_by_id('sign_in').click()
        self.assertIn("http://localhost:8000/dash/login/", self.driver.current_url)

    def tearDown(self):
        self.driver.quit

if __name__ == '__main__':
    unittest.main()