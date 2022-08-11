import unittest

from page_objects.pictures_page import PicturePage
from page_objects.start_page import StartPage
from page_objects.search_page import SearchPage
from webdriver_factory import WebDriverFactory


class PicturesTest(unittest.TestCase):

    def setUp(self) -> None:
        """Действия до теста"""
        self.driver = WebDriverFactory.get_driver()
        self.start_page = StartPage(self.driver)
        self.search_page = SearchPage(self.driver)
        self.picture_page = PicturePage(self.driver)
        self.expected_url = 'https://yandex.ru/images/'

    def tearDown(self) -> None:
        """Действия после теста"""
        self.driver.save_screenshot('test-reports/' + self.id() + '.png')
        # self.driver.close()

    def test_pictures(self):
        """test_pictures"""
        self.start_page.open()
        self.start_page.get_link_pictures().click()
        self.start_page.swich_to_new_window()
        self.assertIn(self.expected_url, self.picture_page.get_current_url())
        self.picture_page.click_categories_result(1)
        self.assertEqual(self.picture_page.get_name_category(1), self.start_page.get_value_search_field())
        self.picture_page.click_expected_picture(1)
        self.assertTrue(self.picture_page.picture_is_present())
        expected_src = self.picture_page.get_src_image()
        self.picture_page.movie_to_next_pictures()
        self.picture_page.movie_to_previous_pictures()
        self.assertEqual(expected_src, self.picture_page.get_src_image())
