from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.base_page import BasePage


class SearchPage(BasePage):

    def get_search_results(self) -> list:
        search_results = self.driver.find_elements(By.XPATH, "//a[@class='Link Link_theme_outer Path-Item link path__item link organic__greenurl']")
        return search_results

    def get_expected_result(self, index):
        href = self.get_search_results()[index - 1].get_attribute("href")
        return href

