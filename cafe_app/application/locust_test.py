import datetime
import json
import time
import random
import json
from locust import HttpUser, task, tag, between


# Статичные данные для тестирования
CLIENT_NAMES = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh']
PRODUCT_NAMES = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh']
CLIENT_EMAILS = ['aaa@mail.ru', 'bbb@mail.ru', 'ccc@mail.ru', 'ddd@mail.ru',
                 'eee@mail.ru', 'fff@mail.ru', 'ggg@mail.ru', 'hhh@mail.ru']


PAYMENT_TYPES = ['SberPay', 'GooglePay', 'Card', 'QR-code']

class RESTServerUser(HttpUser):
    """ Класс, эмулирующий пользователя / клиента сервера """
    wait_time = between(1.0, 5.0)       # время ожидания пользователя перед выполнением новой task

    # Адрес, к которому клиенты (предположительно) обращаются в первую очередь (это может быть индексная страница, страница авторизации и т.п.)
    def on_start(self):
        self.client.get("/docs")    # базовый класс HttpUser имеет встроенный HTTP-клиент для выполнения запросов (self.client)

    @tag("get_all_task")
    @task(3)
    def get_all_task(self):
        """ Тест GET-запроса (получение нескольких записей о клиентах) """
        with self.client.get(f'/api/zoo_cafe/customer',
                             catch_response=True,
                             name='/api/zoo_cafe/customer') as response:
            # Если получаем код HTTP-код 200, то оцениваем запрос как "успешный"
            if response.status_code == 200:
                response.success()
            # Иначе обозначаем как "отказ"
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("get_one_task")
    @task(10)
    def get_one_task(self):
        """ Тест GET-запроса (получение одной записи) """
        client_id = random.randint(0, 7)
        client_email = CLIENT_EMAILS[client_id]
        with self.client.get(f'/api/zoo_cafe/customer/{client_email}',
                             catch_response=True,
                             name='/api/zoo_cafe/customer/{client_email}') as response:
            # Если получаем код HTTP-код 200, то оцениваем запрос как "успешный"
            if response.status_code == 200:
                response.success()
            # Иначе обозначаем как "отказ"
            else:
                response.failure(f'Status code is {response.status_code}')


    @tag("put_task")
    @task(3)
    def put_task(self):
        """ Тест PUT-запроса (обновление записи о продукте) """
        product_id = random.randint(0, 7)
        product_name = PRODUCT_NAMES[product_id]

        test_data = {'product_name': product_name,
                     'desctiption': product_name,
                     'quantity_in_stock': random.randint(1000, 2000),
                     'prime_cost': random.uniform(0.01, 5.99),
                     'final_cost': random.uniform(0.01, 5.99)}

        put_data = json.dumps(test_data)

        # отправляем PUT-запрос
        with self.client.put('/api/zoo_cafe/product',
                             catch_response=True,
                             name='/api/zoo_cafe/product',
                             data=put_data,
                             headers={'content-type': 'application/json'}) as response:
            if response.status_code == 202:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')

    @tag("post_task")
    @task(1)
    def post_task(self):
        payment_type_id = random.randint(0, 3)
        peyment_type = PAYMENT_TYPES[payment_type_id]

        client_id = random.randint(0, 7)
        client_name = CLIENT_NAMES[client_id]

        num_products = random.randint(1, 5)
        products_in_order = []
        for i in range(num_products):
            product_id = random.randint(0, 7)
            product_name = PRODUCT_NAMES[product_id]
            products_in_order.append(product_name)

        """ Тест POST-запроса (создание записи о заказе) """
        # Генерируем случайные данные в опредленном диапазоне
        test_data = {'customer': client_name,
                     'products': products_in_order,
                     'date_time': datetime.datetime.now(),
                     'payment_type': payment_type_id}
        post_data = json.dumps(test_data)       # сериализуем тестовые данные в json-строку
        # отправляем POST-запрос с данными (POST_DATA) на адрес <SERVER>/api/zoo_cafe
        with self.client.post('/api/zoo_cafe/product',
                              catch_response=True,
                              name='/api/zoo_cafe/product', data=post_data,
                              headers={'content-type': 'application/json'}) as response:
            # проверяем корректность возвращаемого HTTP-кода
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f'Status code is {response.status_code}')