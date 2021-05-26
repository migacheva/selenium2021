import time

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
    # chrome_driver = webdriver.Chrome()
    # ie_driver = webdriver.Ie()
    # ie_driver = webdriver.Ie(capabilities={"requireWindowFocus": True})
    # firefox_driver = webdriver.Firefox() #Новая схема
    # wd = webdriver.Firefox(capabilities={"marionette": False}) #Старая схема
    # firefox_driver = webdriver.Firefox(firefox_binary="c:\\Program Files\\Firefox Nightly\\firefox.exe") #Nightly
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://localhost/litecart/admin")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    driver.find_element_by_id("box-apps-menu")
    time.sleep(2)
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located('[title="Logout"]')).click()
    # WebDriverWait(driver, 10).until(EC.title_is("webdriver - Поиск в Google"))
    driver.find_element_by_css_selector('[title="Logout"]').click()
    driver.find_element_by_css_selector('div [class="content"]')


def test_check_all_parts_lab4(driver):
    """
    Задание 7. Сделайте сценарий, проходящий по всем разделам админки
    Сделайте сценарий, который выполняет следующие действия в учебном приложении litecart.
    1) входит в панель администратора http://localhost/litecart/admin
    2) прокликивает последовательно все пункты меню слева, включая вложенные пункты
    3) для каждой страницы проверяет наличие заголовка (то есть элемента с тегом h1)
    """
    driver.get("http://localhost/litecart/admin")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    for section in range(1, len(driver.find_elements_by_css_selector("#app-")) + 1):
        driver.find_element_by_css_selector(f"#app-:nth-child({section})").click()
        if driver.find_elements_by_css_selector(f"#app-:nth-child({section}) li") is not None:
            for sub_section in range(1, len(driver.find_elements_by_css_selector(f"#app-:nth-child({section}) li")) + 1):
                driver.find_element_by_css_selector(f"#app-:nth-child({section}) li:nth-child({sub_section})").click()
                assert driver.find_element_by_css_selector("#content > h1"), "Заголовок H1 не найден"
    driver.find_element_by_css_selector('[title="Logout"]').click()
    driver.find_element_by_css_selector('div [class="content"]')


def test_check_stickers_lab4(driver):
    """
    Задание 8. Сделайте сценарий, проверяющий наличие стикеров у товаров
    Сделайте сценарий, проверяющий наличие стикеров у всех товаров в учебном приложении litecart на главной странице.
    Стикеры -- это полоски в левом верхнем углу изображения товара,
    на которых написано New или Sale или что-нибудь другое.
    Сценарий должен проверять, что у каждого товара имеется ровно один стикер.
    """
    driver.get("http://localhost/litecart/")
    duck = driver.find_elements_by_css_selector('[class="listing-wrapper products"] .link')
    count_stickers = len(driver.find_elements_by_css_selector('[class^="sticker"]'))
    assert len(duck) == count_stickers, f"""   Колличество товаров не соответствует колличеству стикеров. 
                                                Колличество товаров: {len(duck)}
                                                Колличество стикеров: {count_stickers}"""
    for elem in duck:
        assert len(elem.find_elements_by_css_selector('[class^="sticker"]')) == 1, \
            "Для элемента найдено более одного стикера"


