
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from driver_conf import Driver

class ChromeDriver(Driver):
    """ Class for creation ChromeInstance """
    def __init__(self, hidden: bool = False):
        self.__driver = webdriver.Chrome(
            service=self._configure_service(),
            options=self._configure_options(hidden)
        )

    @property
    def driver(self):
        return self.__driver

    def wait_for_element(self, x_path: str, timeout: int = 10) -> WebElement:
        """ Method for get WebElement instance with specified time for waiting it """
        return WebDriverWait(self.driver, timeout).until(expected_conditions.presence_of_element_located(
            (By.XPATH, x_path)
        ))

    def wait_for_element_and_click(self, x_path: str, timeout: int = 10) -> None:
        """ Method for do click on the WebElement instance with specified time for waiting """
        self.wait_for_element(x_path, timeout).click()

    def find_elements_by_xpath(self, x_path: str) -> list[WebElement]:
        return self.driver.find_elements(By.XPATH, x_path)

    def find_element_by_xpath(self, x_path: str) -> WebElement:
        return self.driver.find_element(By.XPATH, x_path)

    @staticmethod
    def _configure_service():
        # 'nt' - the os name for windows:
        if os.name == 'nt':
            return webdriver.ChromeService(executable_path='drivers/windows/chrome/chromedriver.exe')

        # 'posix' - the os name for linux and mac.
        return webdriver.ChromeService(executable_path='drivers/linux/chrome/chromedriver')

    @staticmethod
    def _configure_options(hidden: bool):
        chrome_options = webdriver.ChromeOptions()

        if hidden:
            chrome_options.add_argument('--headless=new')

        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        return chrome_options
