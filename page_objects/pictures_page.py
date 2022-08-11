from typing import List

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from page_objects.base_page import BasePage


class PicturePage(BasePage):

    def get_current_url(self) -> str:
        url = self.driver.current_url
        return url

    def get_categories_results(self) -> list:
        category_results = self.driver.find_elements(By.CLASS_NAME, 'PopularRequestList-Item')
        return category_results

    def get_name_category(self, value) -> str:
        name_category = self.get_categories_results()[value - 1].get_attribute("data-grid-text")
        return name_category

    def click_categories_result(self, value):
        category_result = self.driver.find_elements(By.CLASS_NAME, 'PopularRequestList-Item')[value - 1]
        category_result.click()

    def click_expected_picture(self, index):
        WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//img[@class='serp-item__thumb justifier__thumb']")))
        expected_picture = self.driver.find_elements(By.XPATH, "//img[@class='serp-item__thumb justifier__thumb']")[index - 1]
        expected_picture.click()

    def picture_is_present(self) -> bool:
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "MMImage-Preview")))
        picture = self.driver.find_element(By.CLASS_NAME, "MMImage-Preview")
        return picture.is_displayed()

    def get_src_image(self) -> str:
        src_image = self.driver.find_element(By.CLASS_NAME, "MMImage-Preview").get_attribute("src")
        return src_image

    def movie_to_next_pictures(self):
        movie_to_next_pictures = self.driver.find_element(By.CLASS_NAME, "CircleButton_type_next")
        movie_to_next_pictures.click()

    def movie_to_previous_pictures(self):
        movie_to_next_pictures = self.driver.find_element(By.CLASS_NAME, "CircleButton_type_prev")
        movie_to_next_pictures.click()




