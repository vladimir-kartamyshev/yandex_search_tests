import unittest

from page_objects.start_page import StartPage
from page_objects.search_page import SearchPage
from webdriver_factory import WebDriverFactory


class SearchTest(unittest.TestCase):

    def setUp(self) -> None:
        """Действия до теста"""
        self.driver = WebDriverFactory.get_driver()
        self.start_page = StartPage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.search_query = "Тензор"
        self.expected_url = "https://tensor.ru/"
        self.expected_index = 1  # Ожидаемый результат поиска

    def tearDown(self) -> None:
        """Действия после теста"""
        self.driver.save_screenshot('test-reports/' + self.id() + '.png')
        # self.driver.close()

    def test_search(self):
        """test_search"""
        self.start_page.open()
        self.assertTrue(self.start_page.search_field_is_present_and_clickable())
        self.start_page.send_keys_in_the_search_field(self.search_query)
        self.assertTrue(self.start_page.suggest_is_open())
        self.assertTrue(self.start_page.click_enter_search_field_with_wait())
        self.assertEqual(self.expected_url, self.search_page.get_expected_result(self.expected_index))

