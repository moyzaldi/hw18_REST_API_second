import allure
import requests
from allure_commons.types import AttachmentType
from selene import browser, have

LOGIN = "test_hw@mail.ru"
PASSWORD = "123456"
NAME = "Tatiana"
WEB_URL = "https://demowebshop.tricentis.com"
API_URL = "https://demowebshop.tricentis.com"


def test_login_though_api():
    with allure.step("Login with API"):
        response = requests.post(
            url=API_URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=response.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(response.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with allure.step("Get cookie from API"):
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    with allure.step("Set cookie from API"):
        browser.open(WEB_URL)
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open(WEB_URL)

    with allure.step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))
