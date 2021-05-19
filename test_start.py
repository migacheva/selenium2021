import time

import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver(request):
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

