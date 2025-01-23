import json
import logging
import allure
import pytest
import requests
from allure_commons.types import AttachmentType
from selene import browser, have
from selene.core.query import value


LOGIN = "test_hw@mail.ru"
PASSWORD = "123456"
NAME = "Tatiana"
WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"



@pytest.fixture()
def login_through_api():
    with allure.step("Login with API"):
        response = requests.post(
            url=API_URL + "login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )

        allure.attach(body=response.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(response.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
        logging.info(response.request.url)
        logging.info(response.status_code)
        logging.info(response.text)

    with allure.step("Get cookie from API"):
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    with allure.step("Set cookie from API"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL)

    with allure.step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))

    yield

    with allure.step("Delete cookies"):
        browser.driver.delete_all_cookies()
        assert len(browser.driver.get_cookies()) == 0



def test_add_to_card_with_login(login_through_api):
    with allure.step("Add product to cart via API"):
        payload = {"giftcard_2.RecipientName": NAME,
                  "giftcard_2.RecipientEmail": LOGIN,
                  "giftcard_2.SenderName": NAME,
                  "giftcard_2.SenderEmail": LOGIN,
                  "addtocart_2.EnteredQuantity": 1}
        response = requests.post(
            url=API_URL + "addproducttocart/details/2/1",
            data=payload
        )

        allure.attach(body=response.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(response.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")
        logging.info(response.request.url)
        logging.info(response.status_code)
        logging.info(response.text)

    with allure.step("Get cookie from API"):
        cookie = response.cookies.get("Nop.customer")

    with allure.step("Set cookie from API"):
        browser.open(WEB_URL + "cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL + "cart")


    with allure.step("Checking if an item has been added to the cart with UI"):
        browser.element('.product-name').should(have.text('$25 Virtual Gift Card'))

    with allure.step("Clear shoping cart"):
        item = browser.element("[name='removefromcart'").get(value)
        payload = {"removefromcart": item}

        response = requests.post(API_URL + "cart", data=payload)
        cookie = response.cookies.get("Nop.customer")

        browser.open(WEB_URL + "cart")

        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(WEB_URL + "cart")
        browser.element('.shopping-cart-page').should(have.text("Your Shopping Cart is empty!"))

