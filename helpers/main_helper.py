import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def login_admin(driver):
    driver.get("http://localhost/litecart/admin")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    time.sleep(1)


def fill_simple(driver, locator, text):
    driver.find_element_by_css_selector(locator).click()
    driver.find_element_by_css_selector(locator).send_keys(text)


def splitter_rgb(color0):
    color = color0.split('(')
    color = color[1].split(')')
    rgba = color[0].split(', ')
    return rgba


def waiter(driver, locator, w_time=10):
    wait = WebDriverWait(driver, w_time)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))


def poof(driver, element, w_time=10):
    wait = WebDriverWait(driver, w_time)
    wait.until(EC.staleness_of(element))


def waiter_smart(driver, locator, text, w_time=20):
    wait = WebDriverWait(driver, w_time)
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, locator), text))


def waiter_window(driver, handles, w_time=10):
    wait = WebDriverWait(driver, w_time)
    wait.until(EC.new_window_is_opened(handles))


def check_logs(driver):
    # проверить в логе браузера сообщения (любого уровня)
    # страница с ошибками в логах driver.get("https://ru.wiktionary.org/wiki/%D1%81%D1%82%D0%B0%D1%80%D1%8C%D1%91")
    for log in driver.get_log("browser"):
        # print(log)
        assert log is None, f"Уровень: {log['level']}\n Ошибка: {log['message']}"
