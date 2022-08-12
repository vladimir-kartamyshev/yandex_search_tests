from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.base_page import BasePage


class StartPage(BasePage):

    def get_search_field(self) -> WebElement:
        """Получаем элемент поля поиска"""
        search_field = self.driver.find_element(By.NAME, "text")
        return search_field

    def get_value_search_field(self) -> str:
        """Получаем значение поля поиска"""
        return self.get_search_field().get_attribute('value')

    def search_field_is_present(self) -> bool:
        """Проверяем наличие элемента поля поиска"""
        return self.get_search_field().is_displayed()

    def search_field_is_present_and_clickable(self) -> bool:
        """Здесь я реализовал второй метод проверки с ожиданием на наличие элемента и кликабельности"""
        WebDriverWait(self.driver, 5).until(expected_conditions.element_to_be_clickable(self.get_search_field()))
        return True

    def send_keys_in_the_search_field(self, keys) -> None:
        """Вводим символы в поле поиска"""
        self.get_search_field().send_keys(keys)

    def click_enter_search_field(self) -> bool:
        """Жмем enter в поле поиска и ждем пока страница изменится на страницу поиска"""
        self.get_search_field().send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 5).until(expected_conditions.url_contains('https://yandex.ru/search'))
        return True

    def click_enter_search_field_with_wait(self) -> bool:
        """Жмем enter в поле поиска и ждем пока не появится таблица с результатами поиска"""
        self.get_search_field().send_keys(Keys.ENTER)
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located((By.ID, 'search-result')))
        return True

    def suggest_is_open(self) -> bool:
        """Дожидаемся и проверяем открылись ли поисковые подсказки"""
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'mini-suggest_open')))
        return True

    def get_link_pictures(self) -> WebElement:
        """Получаем элемент кнопки картинки"""
        link_pictures = self.driver.find_element(By.LINK_TEXT, 'Картинки')
        return link_pictures

    def switch_to_new_window(self) -> None:
        """Переключаемся на новую вкладку в браузере"""
        self.driver.switch_to.window(self.driver.window_handles[1])
