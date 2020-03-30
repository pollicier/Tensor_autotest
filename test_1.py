from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# инициализируем драйвер браузера
browser = webdriver.Chrome()
browser.maximize_window()

# задаём через переменную нужную ссылку и открываем её
link = "https://yandex.ru/"
browser.get(link)
browser.implicitly_wait(5)


def do_action(target):
    target_element = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, target)))
    target_click = browser.find_element_by_css_selector(target)
    action = ActionChains(browser)
    action.click(target_click)
    action.perform()
    action.reset_actions()
    return target_element


# чтобы гарантировать корректную работу, используем конструкцию try/finally
try:
    wait = WebDriverWait(browser, 10)
    # проверяем наличие поля поиска
    search_selector = ".input__control.input__input"
    search = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, search_selector)))
    ActionChains(browser).move_to_element(search).perform()
    assert search, "Поле не найдено"

    # вводим в поле поиска нужный запрос
    request = "тензор"
    search.send_keys(request)

    # проверяем, появилась ли таблица с подсказками
    table_selector = "div.mini-suggest__popup-content"
    table = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, table_selector)))
    assert table, "Таблица не найдена"

    # находим кнопку "Найти" и жмём на неё
    find_button_selector = ".button.mini-suggest__button"
    do_action(find_button_selector)

    # проверяем, ведёт ли первая ссылка на сайт tensor.ru
    first_link_selector = "#search-result > li:nth-child(3) > div > h2 > a"
    first_link_target = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, first_link_selector)))
    first_url = first_link_target.get_attribute("href")
    compared_value = "https://tensor.ru/"
    assert first_url == compared_value, "Неправильный сайт"

finally:
    browser.quit()
