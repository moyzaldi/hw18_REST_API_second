import allure
import pytest
import requests
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
        result = requests.post(
            url=API_URL + "login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )

    with allure.step("Get cookie from API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

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



def test_add_to_card_without_login():
    with allure.step("Add product to cart via API"):
        payload = {"giftcard_2.RecipientName": NAME,
                  "giftcard_2.RecipientEmail": LOGIN,
                  "giftcard_2.SenderName": NAME,
                  "giftcard_2.SenderEmail": LOGIN,
                  "addtocart_2.EnteredQuantity": 1}

        result = requests.post(
            url=API_URL + "addproducttocart/details/2/1",
            data=payload
        )

    with allure.step("Get cookie from API"):
        cookie = result.cookies.get("Nop.customer")

    with allure.step("Set cookie from API"):
        browser.open(WEB_URL + "cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

        browser.open(WEB_URL + "cart")

    with allure.step("Checking if an item has been added to the cart with UI"):
        browser.element('[class="product-name"]').should(have.text('$25 Virtual Gift Card'))

    with allure.step("Clear shoping cart"):
        item = browser.element("[name='removefromcart'").get(value)
        payload = {"removefromcart": item}

        result = requests.post(API_URL + "cart", data=payload)
        cookie = result.cookies.get("Nop.customer")

        browser.open(WEB_URL + "cart")

        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(WEB_URL + "cart")
        browser.element("[class='page shopping-cart-page'").should(have.text("Your Shopping Cart is empty!"))


def test_add_to_card_with_login(login_through_api):
    with allure.step("Add product to cart via API"):
        payload = {"giftcard_2.RecipientName": NAME,
                  "giftcard_2.RecipientEmail": LOGIN,
                  "giftcard_2.SenderName": NAME,
                  "giftcard_2.SenderEmail": LOGIN,
                  "addtocart_2.EnteredQuantity": 1}
        result = requests.post(
            url=API_URL + "addproducttocart/details/2/1",
            data=payload
        )

    with allure.step("Get cookie from API"):
        cookie = result.cookies.get("Nop.customer")

    with allure.step("Set cookie from API"):
        browser.open(WEB_URL + "cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL + "cart")


    with allure.step("Checking if an item has been added to the cart with UI"):
        browser.element('[class="product-name"]').should(have.text('$25 Virtual Gift Card'))

    with allure.step("Clear shoping cart"):
        item = browser.element("[name='removefromcart'").get(value)
        payload = {"removefromcart": item}

        result = requests.post(API_URL + "cart", data=payload)
        cookie = result.cookies.get("Nop.customer")

        browser.open(WEB_URL + "cart")

        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(WEB_URL + "cart")
        browser.element("[class='page shopping-cart-page'").should(have.text("Your Shopping Cart is empty!"))

