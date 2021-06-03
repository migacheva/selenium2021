import time


def login_admin(driver):
    driver.get("http://localhost/litecart/admin")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()
    time.sleep(1)


def fill_simple(driver, locator, text):
    driver.find_element_by_css_selector(locator).click()
    driver.find_element_by_css_selector(locator).send_keys(text)