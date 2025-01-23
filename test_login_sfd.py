import allure
import requests
from allure_commons.types import AttachmentType
from selene import browser, have
from selene.core.query import value



LOGIN = "test_hw@mail.ru"
PASSWORD = "123456"
NAME = "Tatiana"
WEB_URL = "https://demowebshop.tricentis.com"
API_URL = "https://demowebshop.tricentis.com"


def test_add_to_card_with_login():
    with allure.step("Login with API"):
        response1 = requests.post(
            url=API_URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )

    with allure.step("Get cookie from API"):
        cookie = response1.cookies.get("NOPCOMMERCE.AUTH")

    with allure.step("Add product to cart with API"):
        response2 = requests.post(
            url=API_URL + "/addproducttocart/details/2/1",
            data={"giftcard_2.RecipientName": NAME,
                  "giftcard_2.RecipientEmail": LOGIN,
                  "giftcard_2.SenderName": NAME,
                  "giftcard_2.SenderEmail": LOGIN,
                  "addtocart_2.EnteredQuantity": 1}
        )

    with allure.step("Assert status code"):
        assert response2.status_code == 200

    with allure.step("Set cookie from API"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})

    with allure.step("Checking if an item has been added to the cart with UI"):
        browser.open(WEB_URL + "/cart")
        browser.element('[class="product-name"]').should(have.text('$25 Virtual Gift Card'))



    with allure.step("Clear shoping cart"):
        item = browser.element("[name='removefromcart'").get(value)
        response3 = requests.post(
            url=API_URL + "/cart",
            data= {'removefromcart': item,
                   'updatecart': 'Update shopping cart',
                   'discountcouponcode': '',
                   'giftcardcouponcode': ''}
        )
