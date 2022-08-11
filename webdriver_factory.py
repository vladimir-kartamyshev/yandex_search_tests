from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

import os

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

WINDOW_SIZES = {
    'DESKTOP_1024X768': {
        'width': 1024,
        'height': 768,
        'deviceScaleFactor': 1,
        'mobile': False
    },
    'DESKTOP_800X600': {
        'width': 800,
        'height': 600,
        'deviceScaleFactor': 1,
        'mobile': False
    },
    'DESKTOP_1280X720': {
        'width': 1280,
        'height': 720,
        'deviceScaleFactor': 1,
        'mobile': False
    },
    'DESKTOP_1920X1080': {
        'width': 1920,
        'height': 1080,
        'deviceScaleFactor': 1,
        'mobile': False
    },
    'MACBOOK_PRO_2017': {
        'width': 2560 / 2,
        'height': 1600 / 2,
        'deviceScaleFactor': 2,
        'mobile': False
    },
    'IPHONE_12_MINI': {
        'width': 360,
        'height': 780,
        'deviceScaleFactor': 3,
        'mobile': True
    },
    'IPHONE_12_MINI_LANDSCAPE': {
        'width': 780,
        'height': 360,
        'deviceScaleFactor': 3,
        'mobile': True
    },
    '300X300': {
        'width': 300,
        'height': 300,
        'deviceScaleFactor': 3,
        'mobile': True
    }
}


class WebDriverFactory:

    @staticmethod
    def get_driver() -> WebDriver:
        """
        :return:  WebDriver — абстрактный класс, от которого унаследованы все другие
        вебдрайверы (Хром, удаленный, Фаерфокс и т. д.)
        """

        # Здесь должен быть алгоритм по которому фабрика выбирает КОНКРЕТУЮ РЕАЛИЗАЦИЮ драйвера.
        # Есть три варианта алгоритма:
        # 1. По дням недели (разумеется шуточный вариант)
        # 2. По переменной окружения DRIVER_KIND (реализовано на BitBucket Pipelines)
        # 3. По аргументам командной строки в момент запуска тестов.

        driver_kind: str = WebDriverFactory.get_driver_kind()
        if driver_kind == "remote":
            driver = WebDriverFactory.get_remote_driver()
        elif driver_kind == "chrome":
            driver = WebDriverFactory.get_chrome_driver()
        elif driver_kind == "firefox":
            driver = WebDriverFactory.get_firefox_driver()
        elif driver_kind == "safari":
            driver = WebDriverFactory.get_safari_driver()
        else:
            raise NotImplemented('Getting driver for ' + driver_kind + ' is not implemented yet.')

        resolution = WebDriverFactory.get_window_resolution()

        driver.set_window_size(
            width=resolution['width'],
            height=resolution['height']
        )
        return driver

    @staticmethod
    def get_driver_kind() -> str:
        """Какой именно Selenium WebDriver нужен в этом запуске тестов?"""
        driver_kind: str = os.environ['SELENIUM_DRIVER_KIND'].lower()
        return driver_kind

    @staticmethod
    def get_window_resolution() -> dict:
        window_config: str = os.environ['WINDOW_RESOLUTION'].upper()
        return WINDOW_SIZES[window_config]

    @staticmethod
    def get_firefox_driver():
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        return driver

    @staticmethod
    def get_chrome_driver():
        options = Options()
        # Отключить графический интерфейс браузера
        # options.add_argument('--headless')
        chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        ret = chrome_driver.execute_cdp_cmd(
            cmd="Emulation.setDeviceMetricsOverride",
            cmd_args=WebDriverFactory.get_window_resolution()
        )

        # Установка геолокации
        WebDriverFactory.set_geolocation(chrome_driver)

        # Установка настроек сетевого соединения
        # chrome_driver.execute_cdp_cmd(
        #     cmd="Network.emulateNetworkConditions",
        #     cmd_args={
        #         'offline': False,
        #         'latency': 2000,
        #         'downloadThroughput': 1000,
        #         'uploadThroughput': 1000
        #     }
        # )

        # # Установка часового пояса
        # chrome_driver.execute_cdp_cmd(
        #     cmd="Emulation.setTimezoneOverride",
        #     cmd_args={
        #         'timezoneId': "Asia/Singapore"
        #     }
        # )
        #
        # # Установка локали
        # chrome_driver.execute_cdp_cmd(
        #     cmd="Emulation.setLocaleOverride",
        #     cmd_args={
        #         'locale': "de_DE"
        #     }
        # )

        return chrome_driver

    @staticmethod
    def set_geolocation(chrome_driver):
        chrome_driver.execute_cdp_cmd(
            cmd="Browser.grantPermissions",
            cmd_args={
                "permissions": ["geolocation"]
            }
        )
        chrome_driver.execute_cdp_cmd(
            cmd="Emulation.setGeolocationOverride",
            cmd_args={
                "latitude": 37.7749,
                "longitude": 122.4194,
                "accuracy": 1000
            }
        )

    @staticmethod
    def get_safari_driver():
        return webdriver.Safari()

    @staticmethod
    def get_remote_driver():
        options = Options()
        options.add_argument('--window-size=850, 1980')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

        # Этот аргумент я добавил, чтобы избежать ошибки "selenium.common.exceptions.
        # WebDriverException: Message: unknown error: session deleted because of page crash"
        # "This will force Chrome to use the /tmp directory instead.
        # This may slow down the execution though since disk will be used instead of memory."
        # https://stackoverflow.com/questions/53902507/unknown-error-session-deleted-because-of-page-crash-from-unknown-error-cannot
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Remote(
            command_executor='http://localhost:3000/webdriver',
            options=options,
        )
        driver.implicitly_wait(10)
        driver.set_window_size(850, 1980)
        return driver