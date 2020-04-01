from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# задаём все переменные, используемые в коде
link = "https://yandex.ru/"
images_selector = "div.home-arrow__tabs a:nth-child(3)"
first_img_selector = "#main > div > div > div:nth-child(1) > div:nth-child(1) > div > a"
img_selector = "div.cl-viewer-image img"
forward_selector = "div.cl-viewer-navigate__item_right"
back_selector = "div.cl-viewer-navigate__item_left"

# инициализируем драйвер браузера
browser = webdriver.Chrome()
browser.maximize_window()
browser.implicitly_wait(15)

# открываем нужную ссылку
browser.get(link)

# создаём функцию для клика по элементу


def do_action(target):
    target_element = WebDriverWait(browser, 15).until(
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
    # проверяем на наличие ссылку "Картинки"
    images_link = browser.find_element_by_css_selector(images_selector)
    try:
        assert images_link, "Ссылка не найдена"
    except AssertionError:
        print("Ссылка не найдена")
        browser.quit()
    images_link = images_link.get_attribute("href")
    browser.get(images_link)

    # кликаем на первую картинку
    do_action(first_img_selector)

    # проверяем, открылась ли картинка
    img = WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, img_selector))
    )
    try:
        assert img, "Картинка не найдена"
    except AssertionError:
        print("Картинка не найдена")
        browser.quit()

    # достаем ссылку первого изображения для дальнейшего сравнения
    first_compared_img = img.get_attribute("src")

    # проверяем наличие и кликаем на кнопку "вперёд"
    try:
        assert do_action(forward_selector), "Нет кнопки 'вперёд'"
    except AssertionError:
        print("Нет кнопки 'вперёд'")
        browser.quit()

    # проверяем, изменилась ли картинка
    second_img = WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, img_selector))
    )
    second_compared_img = second_img.get_attribute("src")
    try:
        assert first_compared_img != second_compared_img, "Изображение не изменилось"
    except AssertionError:
        print("Изображение не изменилось")
        browser.quit()

    # проверяем наличие и кликаем на кнопку "назад"
    try:
        assert do_action(back_selector), "Нет кнопки 'назад'"
    except AssertionError:
        print("Нет кнопки 'назад'")
        browser.quit()

    # проверяем, вернулись ли мы к исходной картинке
    source_img = WebDriverWait(browser, 10).until(
        ec.visibility_of_element_located((By.CSS_SELECTOR, img_selector))
    )
    source_img_comp = source_img.get_attribute("src")
    try:
        assert first_compared_img == source_img_comp, "Изображение не вернулось к исходному"
    except AssertionError:
        print("Изображение не вернулось к исходному")
        browser.quit()

finally:
    browser.quit()
