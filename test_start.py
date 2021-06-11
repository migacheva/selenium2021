import os
import time
from datetime import datetime
import random
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains

from helpers import login_admin, fill_simple, splitter_rgb, waiter, waiter_smart, poof, waiter_window


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
            "Для элемента найдено более одного стикера или не найдено вовсе"


def test_sorted_countries(driver):
    """
    Задание 9. Проверить сортировку стран и геозон в админке
    Сделайте сценарии, которые проверяют сортировку стран и геозон (штатов) в учебном приложении litecart.
    1) на странице http://localhost/litecart/admin/?app=countries&doc=countries
        а) проверить, что страны расположены в алфавитном порядке
        б) для тех стран, у которых количество зон отлично от нуля -- открыть страницу этой страны и там проверить, что зоны расположены в алфавитном порядке
    2) на странице http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones
    зайти в каждую из стран и проверить, что зоны расположены в алфавитном порядке"""
    login_admin(driver)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    table_count = driver.find_elements_by_css_selector('[name="countries_form"] tr')
    list_countries = []
    for i in range(2, len(table_count) - 1):
        list_countries.append(driver.find_element_by_css_selector(f'[name="countries_form"] tr:nth-child({i}) > td:nth-child(5)').text)
        zone = driver.find_element_by_css_selector(f'[name="countries_form"] tr:nth-child({i}) > td:nth-child(6)').text
        if zone != '0':
            list_inside = []
            driver.find_element_by_css_selector(f'[name="countries_form"] tr:nth-child({i}) > td:nth-child(5) > a').click()
            tab = driver.find_elements_by_css_selector('#table-zones.dataTable tr:not(.header)')
            for z in range(2, len(tab)+1):
                list_inside.append(driver.find_element_by_css_selector(f"tr:nth-child({z}) > td:nth-child(3)").text)
            sort_list_inside = sorted(list_inside)
            assert sort_list_inside == list_inside, f"Список не отсортирован для {driver.find_element_by_css_selector(f'[name=countries_form] tr:nth-child({i}) > td:nth-child(5)').text}"
            driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    sorted_list_countries = sorted(list_countries)
    assert list_countries == sorted_list_countries, "Основной список не отсортирован"
    # Пункт 2
    driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
    for i in [2, 3]:
        zone = driver.find_element_by_css_selector(f'tr:nth-child({i}) > td:nth-child(4)').text
        if zone != '0':
            driver.find_element_by_css_selector(f'tr:nth-child({i}) > td:nth-child(3) > a').click()
            list_zones = []
            count_z = driver.find_elements_by_css_selector('#table-zones > tbody > tr')
            for z in range(2, len(count_z)):
                list_zones.append(driver.find_element_by_css_selector(f'tr:nth-child({z}) > td:nth-child(3) [selected="selected"]').text)
            sort_list_zones = sorted(list_zones)
            assert sort_list_zones == list_zones, f"Список не отсортирован"
            driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")


def test_check_open_need_product(driver):
    """
    Задание 10. Проверить, что открывается правильная страница товара
    Сделайте сценарий, который проверяет, что при клике на товар открывается правильная страница товара в учебном приложении litecart.
    Более точно, нужно открыть главную страницу, выбрать первый товар в блоке Campaigns и проверить следующее:
        а) на главной странице и на странице товара совпадает текст названия товара
        б) на главной странице и на странице товара совпадают цены (обычная и акционная)
        в) обычная цена зачёркнутая и серая (можно считать, что "серый" цвет это такой, у которого в RGBa представлении одинаковые значения для каналов R, G и B)
        г) акционная жирная и красная (можно считать, что "красный" цвет это такой, у которого в RGBa представлении каналы G и B имеют нулевые значения)
        (цвета надо проверить на каждой странице независимо, при этом цвета на разных страницах могут не совпадать)
        д) акционная цена крупнее, чем обычная (это тоже надо проверить на каждой странице независимо)
    Необходимо убедиться, что тесты работают в разных браузерах, желательно проверить во всех трёх ключевых браузерах (Chrome, Firefox, IE).
    """
    driver.get("http://localhost/litecart")
    elem = driver.find_element_by_css_selector('#box-campaigns [title="Yellow Duck"]:first-child')
    main_text = elem.find_element_by_css_selector('.name').text
    main_old_cost = elem.find_element_by_css_selector('.regular-price')
    main_sale_cost = elem.find_element_by_css_selector('.campaign-price')
    main_text_old_cost = main_old_cost.text
    main_text_sale_cost = main_sale_cost.text
    main_color_old_cost = main_old_cost.value_of_css_property("color")
    main_color_sale_cost = main_sale_cost.value_of_css_property("color")
    main_style_old_cost = main_old_cost.value_of_css_property("text-decoration-line")
    main_style_sale_cost = main_sale_cost.value_of_css_property("text-decoration-line")
    main_size_old_cost = main_old_cost.value_of_css_property("font-size")
    main_size_sale_cost = main_sale_cost.value_of_css_property("font-size")
    # Проверка зачеркнутости
    assert main_style_old_cost != 'none', "Текст должен быть зачеркнут"
    assert main_style_sale_cost in ['none', ''], "Текст не должен быть зачеркнут"
    # Проверка цветов
    rgba_main_color_old_cost = splitter_rgb(main_color_old_cost)
    rgba_main_color_sale_cost = splitter_rgb(main_color_sale_cost)
    assert rgba_main_color_old_cost[0] == rgba_main_color_old_cost[1] == rgba_main_color_old_cost[2], \
        f"Цвет обычной цены не соответствует ожидаемому, код цвета: {main_color_old_cost}"
    assert rgba_main_color_sale_cost[1] == rgba_main_color_sale_cost[2], \
        f"Цвет акционной цены не соответствует ожидаемому, код цвета: {main_color_sale_cost}"
    # Проверка, что акционная цена крупнее, чем обычная
    assert main_size_old_cost < main_size_sale_cost, "Ожидается, что по размеру обычная цена меньше акционной"
    driver.find_element_by_css_selector('[id="box-campaigns"] [title="Yellow Duck"]:first-child').click()
    detail_text = driver.find_element_by_css_selector("#box-product .title").text
    detail_old_cost = driver.find_element_by_css_selector('.regular-price')
    detail_sale_cost = driver.find_element_by_css_selector('.campaign-price')
    detail_text_old_cost = detail_old_cost.text
    detail_text_sale_cost = detail_sale_cost.text
    detail_color_old_cost = detail_old_cost.value_of_css_property("color")
    detail_color_sale_cost = detail_sale_cost.value_of_css_property("color")
    detail_style_old_cost = detail_old_cost.value_of_css_property("text-decoration-line")
    detail_style_sale_cost = detail_sale_cost.value_of_css_property("text-decoration-line")
    detail_size_old_cost = detail_old_cost.value_of_css_property("font-size")
    detail_size_sale_cost = detail_sale_cost.value_of_css_property("font-size")
    # Проверка зачеркнутости
    assert detail_style_old_cost != 'none', "Текст должен быть зачеркнут"
    assert detail_style_sale_cost in ['none', ''], "Текст не должен быть зачеркнут"
    # Проверка цветов
    rgba_detail_color_old_cost = splitter_rgb(detail_color_old_cost)
    rgba_detail_color_sale_cost = splitter_rgb(detail_color_sale_cost)
    assert rgba_detail_color_old_cost[0] == rgba_detail_color_old_cost[1] == rgba_detail_color_old_cost[2], \
        f"Цвет обычной цены не соответствует ожидаемому, код цвета: {main_color_old_cost}"
    assert rgba_detail_color_sale_cost[1] == rgba_detail_color_sale_cost[2], \
        f"Цвет акционной цены не соответствует ожидаемому, код цвета: {main_color_sale_cost}"
    # Проверка, что акционная цена крупнее, чем обычная
    assert detail_size_old_cost < detail_size_sale_cost, "Ожидается, что по размеру обычная цена меньше акционной"
    # Првоерки на соответствие данных между формами
    assert main_text == detail_text, "Название товара на основной странице и в деталях - отличается"
    assert main_text_old_cost == detail_text_old_cost, \
        "Обычная цена товара на основной странице и в деталях - отличается"
    assert main_text_sale_cost == detail_text_sale_cost, \
        "Акционная цена товара на основной странице и в деталях - отличается"


def test_registration(driver):
    """
    Задание 11. Сделайте сценарий регистрации пользователя
    Сделайте сценарий для регистрации нового пользователя в учебном приложении litecart (не в админке, а в клиентской части магазина).
    Сценарий должен состоять из следующих частей:
        1) регистрация новой учётной записи с достаточно уникальным адресом электронной почты
            (чтобы не конфликтовало с ранее созданными пользователями, в том числе при предыдущих запусках того же самого сценария),
        2) выход (logout), потому что после успешной регистрации автоматически происходит вход,
        3) повторный вход в только что созданную учётную запись,
        4) и ещё раз выход.
    В качестве страны выбирайте United States, штат произвольный. При этом формат индекса -- пять цифр.
    Можно оформить сценарий либо как тест, либо как отдельный исполняемый файл.
    Проверки можно никакие не делать, только действия -- заполнение полей, нажатия на кнопки и ссылки.
    Если сценарий дошёл до конца, то есть созданный пользователь смог выполнить вход и выход -- значит создание прошло успешно.
    В форме регистрации есть капча, её нужно отключить в админке учебного приложения на вкладке Settings -> Security."""
    email = 'Kokoko_' + str(datetime.now().strftime("%Y/%m/%d@%H%M%S.qq"))
    pasw = 'qwerty'
    driver.get("http://localhost/litecart/en/create_account")
    fill_simple(driver, locator='[name="firstname"]', text="Anna")
    fill_simple(driver, locator='[name="lastname"]', text="Kovalchuk")
    fill_simple(driver, locator='[name="address1"]', text="address1")
    fill_simple(driver, locator='[name="postcode"]', text="12345")
    fill_simple(driver, locator='[name="city"]', text="Vladimir")
    driver.find_element_by_css_selector('[class="select2-selection__arrow"]').click()
    fill_simple(driver, '[type="search"]', "united state")
    driver.find_element_by_css_selector('[class="select2-results"] li:first-child').click()
    fill_simple(driver, locator='[name="email"]', text=email)
    fill_simple(driver, locator='[name="phone"]', text="+71112223344")
    fill_simple(driver, locator='[name="password"]', text=pasw)
    fill_simple(driver, locator='[name="confirmed_password"]', text=pasw)
    driver.find_element_by_css_selector('[name="create_account"]').click()
    time.sleep(1)
    driver.find_element_by_css_selector('#box-account li:last-child a').click()
    fill_simple(driver, locator='[name="email"]', text=email)
    fill_simple(driver, locator='[name="password"]', text=pasw)
    driver.find_element_by_css_selector('[value="Login"]').click()
    driver.find_element_by_css_selector('#box-account li:last-child a').click()


def test_add_product(driver):
    """
    Задание 12. Сделайте сценарий добавления товара
    Сделайте сценарий для добавления нового товара (продукта) в учебном приложении litecart (в админке).
    Для добавления товара нужно открыть меню Catalog, в правом верхнем углу нажать кнопку "Add New Product",
    заполнить поля с информацией о товаре и сохранить.
    Достаточно заполнить только информацию на вкладках General, Information и Prices.
    Скидки (Campains) на вкладке Prices можно не добавлять.
    Переключение между вкладками происходит не мгновенно, поэтому после переключения можно сделать небольшую паузу
        (о том, как делать более правильные ожидания, будет рассказано в следующих занятиях).
    Картинку с изображением товара нужно уложить в репозиторий вместе с кодом.
    При этом указывать в коде полный абсолютный путь к файлу плохо, на другой машине работать не будет.
    Надо средствами языка программирования преобразовать относительный путь в абсолютный.
    После сохранения товара нужно убедиться, что он появился в каталоге (в админке).
    Клиентскую часть магазина можно не проверять.
    """
    login_admin(driver)
    driver.find_element_by_css_selector('#app-:nth-child(2) a').click()
    # general
    driver.find_element_by_css_selector('#content .button:nth-child(2)').click()
    time.sleep(1)
    name = f"Котик {datetime.now().strftime('%H:%M:%S')}"
    fill_simple(driver, locator='[name="name[en]"]', text=name)
    fill_simple(driver, locator='[name="code"]', text="CAT")
    driver.find_element_by_css_selector('[name="status"][value="1"]').click()
    rand_cat = random.choice(['cat1', 'cat2', 'cat3', 'cat0'])
    driver.find_element_by_css_selector('[name="new_images[]"]').send_keys(os.getcwd() + f"\\img\\{rand_cat}.jpg")
    # Information
    driver.find_element_by_css_selector("#content  li:nth-child(2) > a").click()
    time.sleep(1)
    driver.find_element_by_css_selector('[name="manufacturer_id"]').click()
    driver.find_element_by_css_selector('[name="manufacturer_id"] [value="1"]').click()
    fill_simple(driver, locator='[name="keywords"]', text="Котики")
    fill_simple(driver, locator='[name="short_description[en]"]', text="Сладенький пирожок")
    fill_simple(driver, locator='[class="trumbowyg-editor"]', text="Самый прекрасный и сладенький пирожочек")
    fill_simple(driver, locator='[name="head_title[en]"]', text="Котечек")
    fill_simple(driver, locator='[name="meta_description[en]"]', text="Китка")
    # price
    driver.find_element_by_css_selector("#content  li:nth-child(4) > a").click()
    time.sleep(1)
    fill_simple(driver, locator='[name="purchase_price"]', text="150")
    driver.find_element_by_css_selector('[name="purchase_price_currency_code"]').click()
    driver.find_element_by_css_selector('[name="purchase_price_currency_code"] [value="USD"]').click()
    fill_simple(driver, locator='[name="prices[USD]"]', text="222")
    fill_simple(driver, locator='[name="prices[EUR]"]', text="333")
    # сохранить изменения
    driver.find_element_by_css_selector('[name="save"]').click()
    # проверить что товар добавлен
    time.sleep(3)
    count = len(driver.find_elements_by_css_selector('.dataTable td:nth-child(3)'))
    list_result = []
    for i in range(2, count + 2):
        content = driver.find_element_by_css_selector(f'.dataTable tr:nth-child({i}) > td:nth-child(3)').get_attribute("textContent")
        list_result.append(content)
    assert ' ' + name in list_result, f"Продукт не был добавлен. Содержание: {list_result}"


def test_buy(driver):
    """
    Задание 13. Сделайте сценарий работы с корзиной
    Сделайте сценарий для добавления товаров в корзину и удаления товаров из корзины.

    1) открыть главную страницу
    2) открыть первый товар из списка
    2) добавить его в корзину (при этом может случайно добавиться товар, который там уже есть, ничего страшного)
    3) подождать, пока счётчик товаров в корзине обновится
    4) вернуться на главную страницу, повторить предыдущие шаги ещё два раза, чтобы в общей сложности в корзине было 3 единицы товара
    5) открыть корзину (в правом верхнем углу кликнуть по ссылке Checkout)
    6) удалить все товары из корзины один за другим, после каждого удаления подождать, пока внизу обновится таблица"""
    for i in [1, 2, 3, 4]:
        driver.get("http://localhost/litecart/")
        driver.find_element_by_css_selector("#box-most-popular li:first-child > a.link").click()
        # Ожидаем что выполнен переход к деталям продукта
        waiter(driver, locator="#box-product .title")
        do = driver.find_element_by_css_selector("span.quantity").text
        if driver.find_element_by_css_selector("#box-product .title").text == 'Yellow Duck':
            driver.find_element_by_css_selector('[name="options[Size]"]').click()
            driver.find_element_by_css_selector('[value="Small"]').click()
        driver.find_element_by_css_selector('[name="add_cart_product"]').click()
        # Дождаться что обновился счетчик в корзине
        waiter_smart(driver, locator="span.quantity", text=str(i))
        posle = driver.find_element_by_css_selector("span.quantity").text
        assert do != posle, "Колличество элементов в корзине не изменилось"
        # print("итерация:", i, "до:", do, "после:", posle)
    assert '4' == driver.find_element_by_css_selector("span.quantity").text, "Что-то не успело добавиться"
    driver.find_element_by_css_selector("#cart > a.link").click()
    count = len(driver.find_elements_by_css_selector('#box-checkout-cart > ul > li'))
    for _ in range(1, count):
        waiter(driver, locator='#order_confirmation-wrapper tr.footer > td:nth-child(2)')
        # Дожидаемся что корзина открыта - запоминаем сумму заказа (максимальная на данном этапе)
        table_cost = driver.find_element_by_css_selector('#order_confirmation-wrapper tr.footer > td:nth-child(2)')
        cost_before = table_cost.text
        # Клик по первому элементу + клик удаление (вейтер не всегда срабатывает, надежнее работает time.sleep(1))
        waiter(driver, locator='#box-checkout-cart li:nth-child(1) > a')
        driver.find_element_by_css_selector('#box-checkout-cart li:nth-child(1) > a').click()
        driver.find_element_by_css_selector('#box-checkout-cart li:nth-child(1) [value="Remove"]').click()
        # Дожидаемся что изменилась сумма заказа
        poof(driver, table_cost)
        cost_after = driver.find_element_by_css_selector('#order_confirmation-wrapper tr.footer > td:nth-child(2)').text
        assert cost_before != cost_after, "Сумма заказа не изменилась"
        # print(_, "cost_before", cost_before, "cost_after", cost_after)
    driver.find_element_by_css_selector('#box-checkout-cart li:nth-child(1) [value="Remove"]').click()


def test_check_links(driver):
    """
    Задание 14. Проверьте, что ссылки открываются в новом окне
    Сделайте сценарий, который проверяет, что ссылки на странице редактирования страны открываются в новом окне.
    Сценарий должен состоять из следующих частей:
        1) зайти в админку
        2) открыть пункт меню Countries (или страницу http://localhost/litecart/admin/?app=countries&doc=countries)
        3) открыть на редактирование какую-нибудь страну или начать создание новой
        4) возле некоторых полей есть ссылки с иконкой в виде квадратика со стрелкой
            -- они ведут на внешние страницы и открываются в новом окне, именно это и нужно проверить.
    Конечно, можно просто убедиться в том, что у ссылки есть атрибут target="_blank".
    Но в этом упражнении требуется именно кликнуть по ссылке, чтобы она открылась в новом окне,
    потом переключиться в новое окно, закрыть его, вернуться обратно, и повторить эти действия для всех таких ссылок.
    Не забудьте, что новое окно открывается не мгновенно, поэтому требуется ожидание открытия окна."""
    login_admin(driver)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_css_selector("#content > div > a").click()
    for i in [2, 3, 6, 7, 8, 9, 10]:
        current_handle1 = driver.current_window_handle
        handles = driver.window_handles
        driver.find_element_by_css_selector(f'form tr:nth-child({i}) i').click()
        waiter_window(driver, handles)
        assert len(driver.window_handles) == 2, f"Новая вкладка не открыта, {driver.window_handles}"
        # переключиться на новую вкладку
        current_handle2 = driver.window_handles[1]
        # для тестирования, что вкладки открываются на самом деле
        time.sleep(1)
        driver.switch_to_window(current_handle2)
        driver.close()
        driver.switch_to_window(current_handle1)
        assert len(driver.window_handles) == 1, f"Новая вкладка не закрыта, {driver.window_handles}"

