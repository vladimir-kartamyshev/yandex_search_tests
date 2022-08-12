from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage


class SearchPage(BasePage):

    def get_search_results(self) -> list:
        """Получаем элементы результатов поиска"""
        search_results = self.driver.find_elements(By.XPATH, "//a[@class='Link Link_theme_outer Path-Item link path__item link organic__greenurl']")
        return search_results

    def get_expected_result(self, index):
        """Получаем ссылку на ожидаемую позицию в результатах поиска"""
        href = self.get_search_results()[index - 1].get_attribute("href")
        return href

