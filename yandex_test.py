import unittest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# задаем все переменные
link = "https://yandex.ru/"
compared_value = "https://tensor.ru/"
request = "тензор"
search_selector = ".input__control.input__input"
table_selector = "body > div.mini-suggest__popup"
find_button_selector = "div.search2__button > button"
first_link_selector = "div.organic.bno > h2 > a.i-bem"


class HomePage(object):

    def __init__(self, driver):
        self.driver = driver

    def search(self, selector):
        search_target = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        # наводим курсор на поле поиска
        ActionChains(self.driver).move_to_element(search_target).click().perform()
        # записываем запрос в поле посика
        search_target.send_keys(request)
        return search_target

    def table(self, selector):
        table_target = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        return table_target

    def do_action(self, selector):
        target_element = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        target_click = self.driver.find_element_by_css_selector(selector)
        action = ActionChains(self.driver)
        action.click(target_click)
        action.perform()
        action.reset_actions()
        return target_element, ResultPage


class ResultPage(object):

    def __init__(self, driver):
        self.driver = driver

    def firstLink(self, selector):
        first_link_target = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        first_url = first_link_target.get_attribute("href")
        return first_url


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(link)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.close()

    def testSearch(self):
        # создаем экземпляр класса HomePage
        home = HomePage(self.driver)
        # проверяем наличие поля поиска
        result_search = home.search(search_selector)
        try:
            assert result_search, "Поле не найдено"
        except AssertionError:
            print("Поле не найдено")
            self.driver.close()
        # проверяем наличие таблицы с подсказками
        result_table = home.table(table_selector)
        try:
            assert result_table, "Таблица не найдена"
        except AssertionError:
            print("Таблица не найдена")
            self.driver.close()
        # находим кнопку "Найти" и кликаем на неё
        home.do_action(find_button_selector)
        # создаем экземпляр класса ResultPage
        search = ResultPage(self.driver)
        # проверяем ведёт ли первая ссылка на сайт tensor.ru
        result_link = search.firstLink(first_link_selector)
        try:
            assert result_link, "Неправильный сайт"
        except AssertionError:
            print("Неправильный сайт")
            self.driver.close()
        print("All tests passed!")
