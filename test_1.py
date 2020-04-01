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

# инициализируем драйвер браузера
browser = webdriver.Chrome()
browser.implicitly_wait(10)
browser.maximize_window()

# задаём через переменную нужную ссылку и открываем её
browser.get(link)


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


# чтобы гарантировать корректную работу, используем конструкцию try/finally
try:
    # проверяем наличие поля поиска
    search = WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, search_selector))
    )
    # наводим курсор на поле поиска
    ActionChains(browser).move_to_element(search).click().perform()
    assert search, "Поле не найдено"

    # вводим в поле поиска нужный запрос
    search.send_keys(request)

    # проверяем, появилась ли таблица с подсказками
    table = WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, table_selector))
    )
    assert table, "Таблица не найдена"

    # находим кнопку "Найти" и жмём на неё
    do_action(find_button_selector)

    # проверяем, ведёт ли первая ссылка на сайт tensor.ru
    first_link_target = WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, first_link_selector))
    )
    first_url = first_link_target.get_attribute("href")
    try:
        assert first_url == compared_value, "Неправильный сайт"
    except AssertionError:
        print("Неправильный сайт")
        browser.quit()

    print("All tests passed!")

finally:
    browser.quit()