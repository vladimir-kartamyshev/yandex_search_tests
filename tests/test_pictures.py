import pytest
from page_objects.pictures_page import PicturePage
from page_objects.start_page import StartPage
from webdriver_factory import WebDriverFactory



TEST_DATA = (
    (1, 1),
)


@pytest.mark.parametrize("expected_category_id,expected_picture_id", TEST_DATA)
def test_picture_search(expected_category_id, expected_picture_id):
    """test_picture_search"""
    driver = WebDriverFactory.get_driver()
    start_page = StartPage(driver)
    picture_page = PicturePage(driver)
    expected_url = 'https://yandex.ru/images/'
    start_page.open()
    start_page.click_button_pictures()
    start_page.switch_to_new_window()
    assert expected_url in picture_page.get_current_url()
    picture_page.click_categories_result(expected_category_id)
    assert picture_page.get_name_category(expected_category_id) == start_page.get_value_search_field()
    picture_page.click_expected_picture(expected_picture_id)
    assert picture_page.picture_is_present()
    expected_src = picture_page.get_src_image()
    picture_page.movie_to_next_pictures()
    picture_page.movie_to_previous_pictures()
    assert expected_src == picture_page.get_src_image()
    driver.quit()
