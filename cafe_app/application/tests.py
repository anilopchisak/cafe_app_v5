from django.test import TestCase, RequestFactory
from django.views import View
from .services.repository_service import *

"""
   Данный модуль реализует "тестовые случаи/ситуации" для модуля repository_service.
   Для создания "тестового случая" необходимо создать отдельный класс, который наследует 
   базовый класс TestCase. Класс django.test.TestCase является подклассом unittest.TestCase 
   стандартного Python модуля для тестирования - unittest.

   Более детально см.: https://docs.djangoproject.com/en/4.1/topics/testing/overview/
"""


class TestCafeRepositoryService(TestCase):

    def setUp(self):
        """ Наследуемый метод setUp определяет инструкции,
            которые должны быть выполнены ПЕРЕД тестированием """
        # создаем тестовые записи
        # update_orders()

        add_customer('Clownito', 'clown@mail.ru')
        add_customer('TRALALA', 'hz')
        add_product('donut', 'donut', 20, 1, 2)
        add_product('coffee', 'coffee', 15, 2, 3)
        add_product('something', 'something', 15, 3, 5)
        add_product('nothing', 'absolutely nothing', 100, 10, 20)
        add_product('tissue', 'tissue', 500, 1, 2)
        add_payment_type('Card')
        add_payment_type('SberPay')
        add_payment_type('GooglePay')
        add_order('Clownito', ['donut', 'donut'], 'Card')

    # def test_get_customer_by_name(self):
    #     customer_by_name = get_customer_by_name('Clownito')
    #     print(customer_by_name)
    #     self.assertIsNotNone(customer_by_name)
    #     self.assertTrue(customer_by_name.id == 1)

    def test_get_customer_by_email(self):
        customer_by_email = get_customer_by_email('hz')
        print('test_get_customer_by_email:\n', customer_by_email, '\n')
        self.assertIsNotNone(customer_by_email)
        self.assertTrue(customer_by_email.id == 2)

    def test_delete_customer_by_email(self):
        delete_customer_by_email('hz')
        customer_by_email = get_customer_by_email('hz')
        print('test_delete_customer_by_email:\n', customer_by_email)
        self.assertIsNone(customer_by_email)

    def test_update_customer(self):
        print('test_update_customer:\n', get_customer_by_email('clown@mail.ru'))
        change_customer_email('clown@mail.ru', 'just a clown')
        customer_by_email = get_customer_by_email('just a clown')
        print('new e-mail:\n', customer_by_email, '\n')
        self.assertIsNotNone(customer_by_email)
        self.assertTrue(customer_by_email.id == 1)

    def test_get_product(self):
        product_by_name = get_product_by_name('donut')
        print('test_get_product:\n', product_by_name, '\n')
        self.assertIsNotNone(product_by_name)
        self.assertTrue(product_by_name.id == 1)

    def test_update_product(self):
        print('test_update_product:\n', get_product_by_name('donut'))
        change_product('donut', 'new donut', 'donuttttt')
        new_product = get_product_by_name('new donut')
        print('new product:\n', new_product, '\n')
        self.assertIsNotNone(new_product)

    def test_delete_product(self):
        delete_product('something')
        product_by_name = get_product_by_name('something')
        print('test_delete_product:\n', product_by_name, '\n')
        self.assertIsNone(product_by_name)

    def test_get_payment_type(self):
        payment_type_by_name = get_payment_type_by_name('GooglePay')
        print('test_get_payment_type:\n', payment_type_by_name, '\n')
        self.assertIsNotNone(payment_type_by_name)
        self.assertTrue(payment_type_by_name.id == 3)

    def test_update_payment_type(self):
        print('test_update_payment_type:\n', get_payment_type_by_name('Card'))
        update_payment_type('Card', 'Bank card')
        new_payment_type = get_payment_type_by_name('Bank card')
        print('new payment type:\n', new_payment_type, '\n')
        self.assertIsNotNone(new_payment_type)

    def test_delete_payment_type(self):
        delete_payment_type_by_name('GooglePay')
        payment_type_by_name = get_payment_type_by_name('GooglePay')
        print('test_delete_payment_type:\n', payment_type_by_name)
        self.assertIsNone(payment_type_by_name)

    def test_create_order(self):
        add_order('Clownito', ['nothing', 'coffee'], 'SberPay')
        order = get_last_order_by_customer_name('Clownito')
        print('test_create_order:\n', order)
        print('products in the order:')
        for product in get_products_from_order(order):
            print(product)
        print(' ')
        self.assertIsNotNone(order)

    def test_update_order(self):
        order = get_last_order_by_customer_name('Clownito')
        print('test_update_order:\n', order)
        # add_product_in_order(order, 'tissue')
        # update_order_cost_by_id(order.id)
        update_order_with_products(order, 'tissue')
        print('new order:\n', get_order_by_id(order.id), '\n')
        self.assertIsNotNone(get_order_by_id(order.id))

    def tearDown(self):
        pass


