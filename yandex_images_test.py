import unittest
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


class HomePage(object):

    def __init__(self, driver):
        self.driver = driver

    def find_link(self, selector):
        images_link = self.driver.find_element_by_css_selector(selector)
        images_link = images_link.get_attribute("href")
        return images_link


class ImagePage(object):

    def __init__(self, driver):
        self.driver = driver

    def do_action(self, selector):
        target_element = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        target_click = self.driver.find_element_by_css_selector(selector)
        action = ActionChains(self.driver)
        action.click(target_click)
        action.perform()
        action.reset_actions()
        return target_element

    def find_first(self, selector):
        img = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        first_compared_img = img.get_attribute("src")
        return first_compared_img

    def forward_button(self, selector):
        image = ImagePage(self.driver)
        button = image.do_action(selector)
        return button

    def image_change(self, selector, comp_img):
        second_img = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        second_compared_img = second_img.get_attribute("src")
        return second_compared_img

    def back_button(self, selector):
        image = ImagePage(self.driver)
        button = image.do_action(selector)
        return button

    def return_to_first(self, selector):
        source_img = WebDriverWait(self.driver, 15).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
        source_img_comp = source_img.get_attribute("src")
        return source_img_comp


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get(link)

    def tearDown(self):
        self.driver.close()

    def testImage(self):
        # создаем экземпляр класса HomePage
        home = HomePage(self.driver)
        # проверяем присутствие ссылки "Картинки" на главной странице
        result_search = home.find_link(images_selector)
        try:
            assert result_search, "Ссылка не найдена"
        except AssertionError:
            print("Ссылка не найдена")
            self.driver.close()
        self.driver.get(result_search)

        # создаем экземпляр класса ImagePage
        image_page = ImagePage(self.driver)
        # кликаем на первое изображение
        image_page.do_action(first_img_selector)
        # проверяем открылась ли картинка и
        # достаем ссылку первого изображения для дальнейшего сравнения
        first_comp_img = image_page.find_first(img_selector)
        try:
            assert first_comp_img, "Картинка не найдена"
        except AssertionError:
            print("Картинка не найдена")
            self.driver.close()
        # проверяем наличие и кликаем на кнопку "вперёд"
        forward_click = image_page.forward_button(forward_selector)
        try:
            assert forward_click, "Нет кнопки 'вперёд'"
        except AssertionError:
            print("Нет кнопки 'вперёд'")
            self.driver.close()
        # проверяем изменилась ли картинка
        second_image = image_page.image_change(img_selector, first_comp_img)
        try:
            assert first_comp_img != second_image, "Изображение не изменилось"
        except AssertionError:
            print("Изображение не изменилось")
            self.driver.close()
        # проверяем наличие и кликаем на копку "назад"
        back_click = image_page.back_button(back_selector)
        try:
            assert back_click, "Нет кнопки 'назад'"
        except AssertionError:
            print("Нет кнопки 'назад'")
            self.driver.close()
        # проверяем, вернулись ли мы к исходному изображению
        return_to_first = image_page.return_to_first(img_selector)
        try:
            assert return_to_first == first_comp_img, "Изображение не вернулось к исходному"
        except AssertionError:
            print("Изображение не вернулось к исходному")
            self.driver.close()
        print("All tests passed!")
