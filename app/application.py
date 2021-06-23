from selenium import webdriver

from helpers.locators import css_btn_remove_elem, css_table_cost, css_cart_detail, css_link_in_preview, \
    css_count_to_shoping, url_litecart, css_go_to_detail, css_title_detail, css_add_cart, css_select_size, \
    css_size_small, css_count_in_cart
from helpers.main_helper import poof, waiter, waiter_smart


class Application:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def quit(self):
        self.driver.quit()


def remove_elem(driver):
    driver.find_element_by_css_selector(css_btn_remove_elem).click()


def get_cost(driver):
    # Дожидаемся что корзина открыта - запоминаем сумму заказа (максимальная на данном этапе)
    tbl_cost = driver.find_element_by_css_selector(css_table_cost)
    cost_before = tbl_cost.text
    return cost_before, tbl_cost


def go_to_cart(driver):
    driver.find_element_by_css_selector(css_cart_detail).click()


def check_remove_elem(cost_before, driver, table_cost):
    # Дожидаемся что изменилась сумма заказа
    poof(driver, table_cost)
    cost_after = driver.find_element_by_css_selector(css_table_cost).text
    assert cost_before != cost_after, "Сумма заказа не изменилась"
    # print(_, "cost_before", cost_before, "cost_after", cost_after)


def select_and_remove_elem(driver):
    # Клик по первому элементу + клик удаление (вейтер не всегда срабатывает, надежнее работает time.sleep(1))
    waiter(driver, locator=css_link_in_preview)
    driver.find_element_by_css_selector(css_link_in_preview).click()
    remove_elem(driver)


def check_count_in_cart(driver, n):
    assert f'{n}' == driver.find_element_by_css_selector(css_count_to_shoping).text, "Что-то не успело добавиться"


def add_to_cart(driver, i):
    driver.get(url_litecart)
    driver.find_element_by_css_selector(css_go_to_detail).click()
    # Ожидаем что выполнен переход к деталям продукта
    waiter(driver, locator=css_title_detail)
    do = driver.find_element_by_css_selector(css_count_to_shoping).text
    check_yellow_duck(driver)
    driver.find_element_by_css_selector(css_add_cart).click()
    # Дождаться что обновился счетчик в корзине
    waiter_smart(driver, locator=css_count_to_shoping, text=str(i))
    posle = driver.find_element_by_css_selector(css_count_to_shoping).text
    assert do != posle, "Колличество элементов в корзине не изменилось"
    # print("итерация:", i, "до:", do, "после:", posle)


def check_yellow_duck(driver):
    if driver.find_element_by_css_selector(css_cart_detail).text == 'Yellow Duck':
        driver.find_element_by_css_selector(css_select_size).click()
        driver.find_element_by_css_selector(css_size_small).click()


def remove_all_elems(driver):
    count = len(driver.find_elements_by_css_selector(css_count_in_cart))
    for _ in range(1, count):
        waiter(driver, locator=css_table_cost)
        cost_before, table_cost = get_cost(driver)
        select_and_remove_elem(driver)
        check_remove_elem(cost_before, driver, table_cost)
    remove_elem(driver)


def add_elems(driver, n):
    for i in range(1, n + 1):
        add_to_cart(driver, i)
