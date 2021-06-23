"""Переделайте созданный в задании 13
сценарий для добавления товаров в корзину и удаления товаров из корзины,
чтобы он использовал многослойную архитектуру.
А именно, выделите вспомогательные классы для работы с главной страницей (откуда выбирается товар),
для работы со страницей товара (откуда происходит добавление товара в корзину),
со страницей корзины (откуда происходит удаление),
и реализуйте сценарий, который не напрямую обращается к операциям Selenium, а оперирует вышеперечисленными объектами-страницами.
"""
import pytest
from selenium import webdriver

from app.application import go_to_cart, check_count_in_cart, add_elems, remove_all_elems


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_buy(driver):
    n = 4
    add_elems(driver, n)
    check_count_in_cart(driver, n)
    go_to_cart(driver)
    remove_all_elems(driver)



