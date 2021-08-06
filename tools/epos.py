#  Nikulin Vasily © 2021

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class EPOS:
    driver: webdriver
    cookies: dict

    def run(self, login: str, password: str):
        """
        Авторизация на сайте ЭПОС.Школа

        :param login: Логин на сайте ЭПОС.Школа (str)
        :param password: Пароль на сайте ЭПОС.Школа (str)
        :return: Сессия браузера (WebDriver)
        """
        opts = webdriver.ChromeOptions()
        opts.headless = True

        self.driver = webdriver.Chrome(options=opts)

        # получаем куки для взаимодействия с ЭПОС.Школа
        self.get_cookies(login, password)

    def get_schedule(self):
        try:
            self.driver.get('https://school.permkrai.ru/student_diary/')
        except selenium.common.exceptions.InvalidSessionIdException:
            return 'bad password'
        except selenium.common.exceptions.TimeoutException:
            return 'timeout'
        schedule = {}
        tables = []
        for i in range(1, 7):
            try:
                tables.append(WebDriverWait(self.driver, 10).until(
                    ec.presence_of_element_located((By.XPATH,
                                                    f'html[1]/body[1]/diary-root['
                                                    f'1]/ezd-main-layout[1]/div[1]/section['
                                                    f'1]/ezd-base-layout[ '
                                                    f'1]/section[1]/div[1]/div[2]/div['
                                                    f'1]/diary-student-diary-content[1]/div[1]/div['
                                                    f'1]/diary-student-diary-day[{i}]/div[1]'))))
            except selenium.common.exceptions.TimeoutException:
                return 'timeout'
        for table in tables:
            data = table.text.split('\n')
            schedule[data[0]] = {'lessons': [],
                                 'homeworks': []}
            for el_id in range(len(data)):
                if el_id < len(data) - 1 and \
                        data[el_id].isdigit() and not data[el_id + 1].isdigit():
                    schedule[data[0]]['lessons'].append(data[el_id + 1])
                    if el_id < len(data) - 2 and \
                            (data[el_id + 2].startswith('ДЗ') or data[el_id + 2].startswith('!ДЗ')):
                        schedule[data[0]]['homeworks'].append(data[el_id + 2].split('ДЗ')[1])
                    else:
                        schedule[data[0]]['homeworks'].append('')
        self.driver.close()
        return schedule

    def get_cookies(self, login: str, password: str):
        self.driver.get('https://school.permkrai.ru')
        login_button = self.driver.find_element_by_xpath("(//div[@class='_2WG0s']//a)[2]")
        login_button.click()

        login_button = self.driver.find_element_by_xpath('//div[contains(text(),"Вход с паролем")]')
        login_button.click()

        email_input = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "(//input[@class='base-input__input'])[1]")))

        password_input = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "(//input[@class='base-input__input'])[2]")))
        login_btn = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.TAG_NAME, "button")))

        email_input.send_keys(login)
        password_input.send_keys(password)
        login_btn.click()

        if self.driver.title != 'ЭПОС.Школа':
            self.driver.close()
            return 'bad credentials'

        else:
            data = self.driver.get_cookies()
            cookies = dict()
            for cookie in data:
                cookies[cookie['name']] = cookie['value']
            self.cookies = cookies
