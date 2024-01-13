from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status

from .services.cafe_service import *
from .serializers import *

# Create your views here.
service = CafeService()

class GetDelAllOrders(GenericAPIView):
    serializer_class = CustomerSerializer    # определяем сериализатор (необходимо для генерирования страницы Swagger)
    renderer_classes = [JSONRenderer]       # определяем тип входных данных

    def get(self, request: Request, customer_name: str) -> Response:
        """ Получение всех заказов клиента """
        response = service.get_all_orders_by_customer(customer_name)
        return Response(data=response.data)

    def delete(self, request: Request, customer_name: str) -> Response:
        """ Удаление всех записей о заказах клиента """
        service.delete_all_orders_by_customer(customer_name)
        return Response(status=status.HTTP_200_OK)

class PostOrder(GenericAPIView):
    serializer_class = OrderWithProductsSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новый заказ """
        serializer = OrderWithProductsSerializer(data=request.data)
        if serializer.is_valid():
            service.add_order(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PutProductInOrder(GenericAPIView):
    # serializer_class = ProductSerializer
    renderer_classes = [JSONRenderer]

    def put(self, request: Request, order_id: int, product_name: str) -> Response:
        """ Добавить продукт в заказ """
        order = get_order_by_id(order_id)
        product = get_product_by_name(product_name)
        if order is not None and product is not None:
            service.add_product_in_order(order_id, product_name)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

# Customers
class GetPostPutCustomer(GenericAPIView):
    serializer_class = CustomerSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request) -> Response:
        """ Получение данных обо всех пользователях """
        response = service.get_all_customers()
        return Response(data=response.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить нового пользователя сервиса """
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            service.add_customer(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """ Изменение данных пользователя по имени или адресу электронной почты """
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            name = service.get_customer_by_name(serializer.data.get('customer_name'))
            email = service.get_customer_by_email(serializer.data.get('email'))
            if name is not None and email is None:
                service.update_customer_email(serializer)
            elif name is None and email is not None:
                service.update_customer_name(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetDelCustomerByName(GenericAPIView):
    serializer_class = CustomerSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, customer_name: str) -> Response:
        """ Получение данных о пользователе по имени """
        response = service.get_customer_by_name(customer_name)
        if response is not None:
            print(response.data)
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, customer_name: str) -> Response:
        """ Удаление данных пользователя по имени """
        service.delete_customer_by_name(customer_name)
        return Response(status=status.HTTP_200_OK)

class GetDelCustomerByEmail(GenericAPIView):
    serializer_class = CustomerSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, email: str) -> Response:
        """ Получение данных о пользователе по адресу электронной почты """
        response = service.get_customer_by_email(email)
        if response is not None:
            print(response.data)
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, email: str) -> Response:
        """ Удаление данных пользователя по адресу электронной почты """
        service.delete_customer_by_email(email)
        return Response(status=status.HTTP_200_OK)


# Products
class GetPostPutProduct(GenericAPIView):
    serializer_class = ProductSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request) -> Response:
        """ Получение информации обо всех продуктах """
        response = service.get_all_products()
        return Response(data=response.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новый продукт """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            result = service.add_product(serializer)
            return Response(data=result.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """ Изменение информации о продукте """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            service.update_product_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetDelProduct(GenericAPIView):
    serializer_class = ProductSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, product_name: str) -> Response:
        """ Получение информации о продукте по названию """
        response = service.get_product_by_name(product_name)
        if response is not None:
            print(response.data)
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, product_name: str) -> Response:
        """ Удаление продукта по названию """
        service.delete_product(product_name)
        return Response(status=status.HTTP_200_OK)


# Payment types
class GetPostPaymentType(GenericAPIView):
    serializer_class = PaymentTypeSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request) -> Response:
        """ Получение всех доступных типов оплаты """
        response = service.get_all_payment_types()
        return Response(data=response.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новый тип оплаты """
        serializer = PaymentTypeSerializer(data=request.data)
        if serializer.is_valid():
            service.add_payment_type(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DelPaymentType(GenericAPIView):
    serializer_class = PaymentTypeSerializer
    renderer_classes = [JSONRenderer]

    def delete(self, request: Request, payment_type_name: str) -> Response:
        """ Удалить тип оплаты """
        service.delete_payment_type(payment_type_name)
        return Response(status=status.HTTP_200_OK)


# Payments
class GetPayment(GenericAPIView):
    serializer_class = PaymentSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, order_id: int) -> Response:
        """ Получение всех доступных типов оплаты """
        response = service.get_payment(order_id)
        if response is not None:
            Response(data=response.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
