from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# задаём все переменные, используемые в коде
link = "https://yandex.ru/"
search_selector = ".input__control.input__input"
table_selector = "div.mini-suggest__popup-content"
find_button_selector = ".button.mini-suggest__button"
first_link_selector = "#search-result > li:nth-child(3) > div > h2 > a"
request = "тензор"
compared_value = "https://tensor.ru/"

# инициализируем драйвер браузера
browser = webdriver.Chrome()
browser.maximize_window()
browser.implicitly_wait(15)


# помещаем тестовые сценарии в функции


def do_action(target):
    target_element = WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, target))
    )
    target_click = browser.find_element_by_css_selector(target)
    action = ActionChains(browser)
    action.click(target_click)
    action.perform()
    action.reset_actions()
    return target_element


class TestMainPage(object):

    def test_find_search(self, selector, query):
        browser.get(link)
        search = WebDriverWait(browser, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        ActionChains(browser).move_to_element(search).perform()
        assert search, "Поле не найдено"
        search.send_keys(query)

    def test_table(self, selector):
        table = WebDriverWait(browser, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, table_selector))
        )
        assert table, "Таблица не найдена"

    def test_first_link(self, selector, value_for_comparison):
        first_link_target = WebDriverWait(browser, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        first_url = first_link_target.get_attribute("href")
        assert first_url == value_for_comparison, "Неправильный сайт"


try:
    if __name__ == "__main__":
        # создаём экземпляр класса
        test = TestMainPage()
        # проверяем наличие поля поиска
        test.test_find_search(search_selector, request)
        # проверяем, появилась ли таблица с подсказками
        test.test_table(table_selector)
        # находим кнопку "Найти" и жмём на неё
        do_action(find_button_selector)
        # проверяем, ведёт ли первая ссылка поиска на сайт tensor.ru
        test.test_first_link(first_link_selector, compared_value)
        # если все тесты пройдены успешно, выводим на экран сообщение
        print("All tests passed!")
finally:
    browser.quit()
