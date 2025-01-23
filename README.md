# hw18_REST_API_second
1. Написать несколько тестов на demoshop на добавление товаров в корзину через API с проверкой корзины через UI.

2. Автоматизировать у себя в коде логирование в allure

3. Задача со *: реализовать логирование реквеста в аллюр и в консоль https://demowebshop.tricentis.com/

    with allure.step("Removing an item from the shopping cart"):
        item= browser.element("[name='removefromcart'").get(value)
        response3 = requests.post(
            url=API_URL + "cart",
            data={"removefromcart": item,
                  "updatecart": "Update shopping cart"
                                   }
        )
    time.sleep(5)
