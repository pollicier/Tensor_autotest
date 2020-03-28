from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# инициализируем драйвер браузера
browser = webdriver.Chrome()
browser.maximize_window()

# заходим на нужный сайт по ссылке link
link = "https://yandex.ru/"
browser.get(link)


def do_action(target):
    target_element = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, target)))
    target_click = browser.find_element_by_css_selector(target)
    action = ActionChains(browser)
    action.click(target_click)
    action.perform()
    action.reset_actions()
    return target_element


try:
    wait = WebDriverWait(browser, 10)
    # проверяем на наличие ссылку "Картинки"
    images_selector = "div.home-arrow__tabs a:nth-child(3)"
    images_link = browser.find_element_by_css_selector(images_selector)
    images_link = images_link.get_attribute("href")
    browser.get(images_link)
    assert images_link, "Ссылка не найдена"

    # кликаем на первую картинку
    first_img_selector = "#main > div > div > div:nth-child(1) > div:nth-child(1) > div > a"
    do_action(first_img_selector)

    # проверяем, открылась ли картинка
    img_selector = "div.cl-viewer-image img"
    img = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, img_selector)))
    assert img, "Картинка не найдена"

    # достаем ссылку первого изображения для дальнейшего сравнения
    first_compared_img = img.get_attribute("src")

    # создаём CSS-селекторы для кнопок "вперёд" и "назад"
    forward_selector = "div.cl-viewer-navigate__item_right"
    back_selector = "div.cl-viewer-navigate__item_left"

    # проверяем наличие и кликаем на кнопку "вперёд"
    assert do_action(forward_selector), "Нет кнопки 'вперёд'"

    # проверяем, изменилась ли картинка
    second_img = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, img_selector)))
    second_compared_img = second_img.get_attribute("src")
    assert first_compared_img != second_compared_img, "Изображение не изменилось"

    # проверяем наличие и кликаем на кнопку "назад"
    assert do_action(back_selector), "Нет кнопки 'назад'"

    # проверяем, вернулись ли мы к исходной картинке
    source_img = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, img_selector)))
    source_img_comp = source_img.get_attribute("src")
    assert first_compared_img == source_img_comp, "Изображение не вернулось к исходному"

finally:
    browser.quit()
