import os
from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    """Базовый (родительский) класс PageObject,
        который содержит общие для всех страниц методы."""

    def __init__(self, driver: WebDriver):
        """Конструктор класса"""
        self.driver = driver

    def get_base_url(self) -> str:
        """Переменная базовый url"""
        return os.environ['BASE_URL']

    def open(self):
        """Открыть страницу"""
        self.driver.get(self.get_base_url())
