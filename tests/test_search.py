import pytest
from page_objects.start_page import StartPage
from page_objects.search_page import SearchPage
from webdriver_factory import WebDriverFactory


TEST_DATA = (
    ("Тензор", "https://tensor.ru/", 1),
)


@pytest.mark.parametrize("search_query,expected_url,expected_index", TEST_DATA)
def test_search(search_query, expected_url, expected_index):
    """test_search"""
    driver = WebDriverFactory.get_driver()
    start_page = StartPage(driver)
    search_page = SearchPage(driver)
    start_page.open()
    assert start_page.search_field_is_present_and_clickable()
    start_page.send_keys_in_the_search_field(search_query)
    assert start_page.suggest_is_open()
    assert start_page.click_enter_in_search_field_with_wait()
    assert expected_url == search_page.get_expected_result(expected_index)
    driver.quit()
