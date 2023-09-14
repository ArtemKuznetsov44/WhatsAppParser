from main import ABC, abstractmethod, WebDriver, WebElement


class Driver(ABC):
    """ This class is the base class for any other drivers: Chrome, FireFox ond so on """

    def close(self) -> None:
        """ Method for close our driver windows """
        self.driver.close()

    def quite(self):
        """ Method for finishing any process in our driver """
        self.driver.quite()

    @property
    @abstractmethod
    def driver(self):
        pass

    @staticmethod
    @abstractmethod
    def _configure_service():
        """ Method for service configuration """
        pass

    @staticmethod
    @abstractmethod
    def _configure_options(hidden: bool):
        """ Method for options configuration """
        pass

    @abstractmethod
    def wait_for_element(self, x_path: str, timeout: int = 10) -> WebElement:
        """ Method for wait some element with timeout """
        pass

    @abstractmethod
    def wait_for_element_and_click(self, x_path: str, timeout: int = 10) -> None:
        """ Method for wait some element with timeout and click on it """
        pass

    @abstractmethod
    def find_elements_by_xpath(self, x_path: str) -> list[WebElement]:
        """ Method for finding all elements with such XPath on the page """
        pass

    @abstractmethod
    def find_element_by_xpath(self, x_path: str) -> WebElement:
        """ Method for finding one element with such XPath """
        pass
