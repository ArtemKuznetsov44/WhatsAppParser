from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# For make locator specification:
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from chrome_driver import ChromeDriver
# from tqdm import tqdm
from console import os, console_clear
from time import sleep
# Данный класс выступает в роли контекстного процессора, который при старте входит на страницу
# WatsApp, ожидает появление строки поиска (т.е. ждет, пока пользователь отсканирует QR).
# План работы программы:

'''
План работы программы: 
1. При старте - подгружается страница с QR (программа ожидает появления элемента по XPath - строки поиска диалога, т.е.
когда пользователь его от сканирует и войдет в аккаунт)
2. 
'''


class WhatsAppParser:
    """ WhatsApp parser class:
    1. show_all_options() - method for getting list of options
    2. show_all_dialogs() - method for getting list of user's contacts in WhatsApp
    """

    __options = {
        1: 'Выбрать список контактов;',
        2: 'Получить все содержимое переписки по указанному контакту;',
        3: 'Выбрать содержимое переписки по контакту с указанной даты;',
        -1: 'Выход'
    }

    def __init__(self, hidden=False):
        self.__driver = ChromeDriver(hidden)
        self.__searchbar = None
        self.__chats_panel = None

    # Method that is called when we create context manager with <WITH>:

    def __enter__(self):
        self.open()
        return self

    # Method which is called when all code blocks in context manager will be finished:
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Нужно будет реализовать выход из аккаунта пользователя
        self.close()

    def close(self):
        self.__driver.close()
        self.__driver.quit()

    def open(self):
        """ Method for get in WhatsApp web application |  Notice: User have only 60 secs for scan QR-code and get in """

        self.__driver.get('https://web.whatsapp.com')

        if self.__driver.wait_for_element(
                '/html/body/div[1]/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/p',
                60) is None:
            raise NoSuchElementException

    # Method for getting all messages from specified dialog only:
    def get_all_from_specified_dialog(self, contact: str):
        """ Main method for operations with getting data from current dialog """
        # Wait and click for SPECIFIED contact:
        self.__driver.wait_for_element_and_click(
            f'//div[@class="_8nE1Y"]/div[@role="gridcell"]/div[@class="_21S-L"]/span[@title="{contact}"]',
            timeout=30)

        sleep(2)

        # For remaking and rebuilding !
        # dialog_data = (self.__driver.find_element(
        #     By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]').
        # find_elements(
        #     By.XPATH,
        #     './/div[contains(@class, "_1jHIY") and contains(@class, "_2OvAm") and contains(@class, "focusable-list-item")]/div/span | .//div[@class="" and @role="row"]'
        # )
        # )
        #
        # d = {}
        # current_date = ""
        # d_for_row = {}
        # count_per_date = 1
        #
        # for el in dialog_data:
        #
        #     if el.get_attribute('class') == "_11JPr" and el.text not in d:
        #         current_data = el.text.strip()
        #         d[current_data] = list()
        #         count_per_date = 0
        #
        #     d[current_data].append(self.__get_message_content(element=el, number=count_per_date))
        #     count_per_date += 1
        #
        # return d

    def __get_message_content(self, element: WebElement, number: int):
        """ Method for work with current message like bs instance """

        from_user_to_you = False
        images = None
        text_element = None

        try:
            element.find_element(By.XPATH, './/div/div[contains(@class, "message-out")]')
        except NoSuchElementException:
            from_user_to_you = True

        try:
            buttons_for_download = element.find_elements(By.XPATH,
                                                         './/button[@class="gndfcl4n g8xmoczg a9yjteo0 pox2cllw pi22tx4b oov82czi k17s6i4e i86elurf ovllcyds qmp0wt83 i5tg98hk tcyu26xv przvwfww rn41jex5 g0rxnol2 fewfhwl7 ajgl1lbb"]')
            # В цикле проходим по всем кнопкам загрузки изображений:
            for button in buttons_for_download:
                button.click()
                self.__driver.implicitly_wait(2)

        except NoSuchElementException:
            pass

        try:
            images = element.find_elements(By.XPATH,
                                           './/img[@class="jciay5ix tvf2evcx oq44ahr5 lb5m6g5c osz0hll6 nq7eualt em5jvqoa a21kwdn32"]')

            images = [el.get_attribute('src') for el in images]
        except NoSuchElementException:
            pass

        try:

            text_element = element.find_element(By.XPATH, './/span[@class="_11JPr selectable-text copyable-text"]')
            text_element = text_element.text

        except NoSuchElementException:
            pass

        res = f"{'#' * 5} №{number} From USER to YOU: {'#' * 5}\n" if from_user_to_you else f"{'#' * 5} №{number} From YOU to USER {'#' * 5}\n"

        if images:
            res += '\n'.join(images)
        if text_element:
            res += f"SMS: {text_element}"

    # Method for getting all user's dialogs:
    def show_all_dialogs(self):
        dialogs = list(filter(
            lambda x: x != 'Unknown subject',
            [el.text for el in self.__driver.find_elements(
                By.XPATH,
                '//div[@class="_21S-L"]/span[@title and @dir="auto" and @aria-label]'
            )]
        ))

        for i, el in enumerate(dialogs):
            print(f"{i + 1}: {el};")

    # Getting service by user's OPERATING SYSTEM:
    @staticmethod
    def __get_service_by_os() -> webdriver.ChromeService:
        # 'nt' - the os name for windows:
        if os.name == 'nt':
            return webdriver.ChromeService(executable_path='drivers/windows/chrome/chromedriver.exe')

        # 'posix' - the os name for linux and mac.
        return webdriver.ChromeService(executable_path='drivers/linux/chrome/chromedriver')

    # Method for printing all available in class options for user:
    @staticmethod
    def show_options():
        for key, value in WhatsAppParser.__options.items():
            print(f"{key}: {value}")


if __name__ == '__main__':
    print(WhatsAppParser.__doc__)
    with WhatsAppParser(hidden=False) as parser:
        while True:
            console_clear()
            parser.show_options()
            user_input = int(input('Введите ключ опции: '))
            # To parse all available contacts:
            if user_input == 1:
                parser.show_all_dialogs()
            # To parse specified dialog:
            elif user_input == 2:
                input_contact = input().strip()
                print(parser.get_all_from_specified_dialog(contact=input_contact))
                pass
            # To parse specified dialog from specified date:
            elif user_input == 3:
                pass
            elif user_input == -1:
                break
