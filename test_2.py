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

# помещаем тестовые сценарии в функции


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


class TestMainPage1(object):

    def __init__(self):
        pass

    def test_find_images_link(self, imgs_selector):
        browser.get(link)
        images_link = browser.find_element_by_css_selector(imgs_selector)
        images_link = images_link.get_attribute("href")
        assert images_link, "Ссылка не найдена"
        browser.get(images_link)

    def test_find_first_image(self, any_img_selector):
        img = WebDriverWait(browser, 15).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, any_img_selector))
        )
        first_compared_img = img.get_attribute("src")
        assert img, "Картинка не найдена"
        return first_compared_img

    def test_forward_button_exist(self, button_selector):
        assert do_action(button_selector), "Нет кнопки 'вперёд'"

    def test_back_button_exist(self, button_selector):
        assert do_action(button_selector), "Нет кнопки 'назад'"

    def test_change_img(self, any_img_selector, comp_img):
        second_img = WebDriverWait(browser, 15).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, any_img_selector))
        )
        second_compared_img = second_img.get_attribute("src")
        assert comp_img != second_compared_img, "Изображение не изменилось"

    def test_return_to_first_img(self, any_img_selector, comp_img):
        source_img = WebDriverWait(browser, 15).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, any_img_selector))
        )
        source_img_comp = source_img.get_attribute("src")
        assert comp_img == source_img_comp, "Изображение не вернулось к исходному"


try:
    if __name__ == "__main__":
        # создаём экземпляр класса
        test = TestMainPage1()
        # проверяем на наличие ссылку "Картинки"
        test.test_find_images_link(images_selector)
        # кликаем на первую картинку
        do_action(first_img_selector)
        # проверяем, открылась ли картинка и
        # достаем ссылку первого изображения для дальнейшего сравнения
        compared_img = test.test_find_first_image(img_selector)
        # проверяем наличие и кликаем на кнопку "вперёд"
        test.test_forward_button_exist(forward_selector)
        # проверяем, изменилась ли картинка
        test.test_change_img(img_selector, compared_img)
        # проверяем на наличие и кликаем на кнопку "назад"
        test.test_back_button_exist(back_selector)
        # проверяем, вернулись ли мы к исходному изображению
        test.test_return_to_first_img(img_selector, compared_img)
        # если все тесты пройдены успешно, выводим на экран сообщение
        print("All tests passed!")

finally:
    browser.quit()
