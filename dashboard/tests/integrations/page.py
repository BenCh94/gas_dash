from element import BasePageElement


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver


class LandingPage(BasePage):
    """Home page action methods come here. I.e. Python.org"""

    def has_sign_in(self):
        # some stuff here
        one = 1
    	 


class DashboardPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source