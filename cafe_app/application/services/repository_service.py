from typing import Optional, Iterable, List
from datetime import datetime
from django.db.models import QuerySet
# Импортируем модели DAO
from ..models import *


# Orders
def get_order_by_id(order_id: int) -> Optional[Order]:
    order = Order.objects.filter(id=order_id).first()
    return order

def get_order_by_customer_id(customer_id: int) -> Optional[Order]:
    order = Order.objects.filter(customer_id=customer_id).first()
    return order

def get_all_orders_by_customer_name(customer_name: str) -> QuerySet:
    customer = get_customer_by_name(customer_name)
    orders = Order.objects.filter(customer_id=customer.id).all()
    return orders

def get_last_order_by_customer_name(customer_name: str) -> Optional[Order]:
    customer = get_customer_by_name(customer_name)
    order = Order.objects.filter(customer_id=customer.id).last()
    return order

def delete_order_by_id(order_id: int) -> None:
    order = Order.objects.filter(id=order_id).first()
    order.delete()

def delete_order_by_customer_name(customer: str) -> None:
    order = get_last_order_by_customer_name(customer)
    order_id = order.id
    delete_order_with_products(order_id)
    order.delete()

def update_all_orders() -> None:
    for order in Order.objects.all():
        order_id = order.id
        full_order = OrderProduct.objects.filter(order_product__order_id=order_id).all()
        full_cost = 0
        for cur_product_in_order in full_order:
            product_id = cur_product_in_order.product_id
            product = cur_product_in_order.select_related('product').filter(product__product_id=product_id).first
            full_cost += product.final_cost
        order.order_cost = full_cost
        order.save()

def update_order_cost_by_id(order_id: int) -> None:
    order = Order.objects.filter(id=order_id).first()
    full_order = OrderProduct.objects.filter(order_id=order_id).all()
    full_cost = 0
    for cur_product_in_order in full_order:
        product = Product.objects.filter(id=cur_product_in_order.product_id.id).first()
        # print(product)
        # print(product.final_cost)
        full_cost += product.final_cost
        # print(full_cost)
    order.order_cost = full_cost
    # print(order)
    order.save()

def add_order(customer_name: str, products: [str], payment_type: str, date_time: datetime):
    customer_id = get_customer_by_name(customer_name)
    # date_time = date_time
    # new order
    order = Order.objects.create(customer_id=customer_id, order_cost=0, date_time=date_time)
    # new payment
    add_payment(order_id=order, payment_type=payment_type)
    # adding all the products and calculating the cost
    for product in products:
        add_product_in_order(order.id, product)
    update_order_cost_by_id(order.id)

# def delete_order(order_id: int) -> None:
#     Order.objects.filter(id=order_id).first().delete()

def delete_all_orders_by_customer(name: str) -> None:
    customer = get_customer_by_name(name)
    orders = Order.objects.filter(customer_id=customer.id).all()
    for order in orders:
        order.delete()

# Customers
def get_all_customers() -> QuerySet:
    result = Customer.objects.all()
    return result

def get_customer_by_order(order_id: int) -> Optional[Customer]:
    order = get_order_by_id(order_id)
    customer = Customer.objects.filter(id=order.customer_id.id).first()
    return customer

def add_customer(name: str, email: str) -> None:
    customer = Customer.objects.create(customer_name=name, email=email)
    customer.save()

def get_customer_by_email(email: str) -> Optional[Customer]:
    customer = Customer.objects.filter(email=email).first()
    return customer

def get_customer_by_name(name: str) -> Optional[Customer]:
    customer = Customer.objects.filter(customer_name=name).first()
    return customer

def delete_customer_by_email(email: str) -> None:
    get_customer_by_email(email).delete()

def delete_customer_by_name(name: str) -> None:
    get_customer_by_name(name).delete()

def change_customer_email(cur_email: str, new_email: str) -> None:
    customer = get_customer_by_email(cur_email)
    customer.email = new_email
    customer.save()

def change_customer_name(cur_name: str, new_name: str) -> None:
    customer = get_customer_by_name(cur_name)
    customer.customer_name = new_name
    customer.save()


# Payment types
def get_all_payment_types() -> PaymentType:
    return PaymentType.objects.all()

def add_payment_type(new_type: str) -> None:
    PaymentType.TYPES.append(new_type)
    payment_type = PaymentType.objects.create(payment_type=PaymentType.TYPES[-1])
    payment_type.save()

def get_payment_type_by_order(order_id: int) -> Optional[PaymentType]:
    payment = get_payment(order_id)
    payment_type = PaymentType.objects.filter(id=payment.payment_type_id.id).first()
    return payment_type

def get_payment_type_by_name(type_name: str) -> Optional[PaymentType]:
    payment_type = PaymentType.objects.filter(payment_type=type_name).first()
    return payment_type

def get_payment_type_by_id(type_id: int) -> Optional[PaymentType]:
    payment_type = PaymentType.objects.filter(id=type_id).first()
    return payment_type

def delete_payment_type_by_name(type_name: str) -> None:
    get_payment_type_by_name(type_name).delete()

def delete_payment_type_by_id(type_id: int) -> None:
    get_payment_type_by_id(type_id).delete()

def update_payment_type(cur_type_name: str, new_type_name: str) -> None:
    payment_type = get_payment_type_by_name(cur_type_name)
    payment_type.payment_type = new_type_name
    payment_type.save()


# Payments
def add_payment(order_id: Order, payment_type: str) -> None:
    payment_type_fk = get_payment_type_by_name(payment_type)
    # order = get_order_by_id(order_id)
    # print(payment_type_fk)
    # print(order)
    payment = Payment.objects.create(order_id=order_id, payment_type_id=payment_type_fk)
    payment.save()

def get_payment(order_id: int) -> Optional[Payment]:
    payment = Payment.objects.filter(order_id=order_id).first()
    return payment

def update_payment(order_id: int, payment_type: str) -> None:
    payment = Payment.objects.filter(order_id=order_id).first()
    payment.payment_type_id = get_payment_type_by_name(payment_type).id
    payment.save()


# Products in order
def add_product_in_order(order_id: int, product_name: str) -> None:
    product = Product.objects.filter(product_name=product_name).first()
    order = Order.objects.filter(id=order_id).first()
    product_in_order = OrderProduct.objects.create(order_id=order, product_id=product)
    # print(product_in_order)
    product_in_order.save()
    remove_product_from_stock(product_name)

def delete_product_from_order(order_id: int, product_name: str) -> None:
    product_id = Product.objects.filter(product_name=product_name)
    OrderProduct.objects.filter(order_id=order_id, product_id=product_id).delete()

def change_product_in_order(order_id: int, cur_product_name: str, new_product_name: str) -> None:
    delete_product_from_order(order_id, cur_product_name)
    add_product_in_order(order_id, new_product_name)

def get_products_from_order(order_id: int) -> QuerySet:
    products_in_order = OrderProduct.objects.filter(order_id=order_id).all()
    products = []
    for product_in_order in products_in_order:
        product = Product.objects.filter(id=product_in_order.product_id.id).first()
        products.append(product)
    # products = Product.objects.select_related('order_product').filter(order_product__order_id=order_id).all()
    return products

def delete_order_with_products(order_id: int) -> None:
    OrderProduct.objects.filter(order_id=order_id).all.delete()

def update_order_with_products(order_id: int, product_name: str) -> None:
    add_product_in_order(order_id, product_name)
    update_order_cost_by_id(order_id.id)


# Products
def get_all_products() -> QuerySet:
    result = Product.objects.all()
    return result

def add_product(name: str, description: str, quantity: int, prime_cost: int, final_cost: int) -> None:
    product = Product.objects.create(product_name=name, description=description,
                                     quantity_in_stock=quantity, prime_cost=prime_cost, final_cost=final_cost)
    product.save()
    return product

def get_product_by_name(name: str) -> Optional[Product]:
    product = Product.objects.filter(product_name=name).first()
    return product

def get_product_by_description(description: str) -> Optional[Product]:
    product = Product.objects.filter(description=description).first()
    return product

def delete_product(name: str) -> None:
    get_product_by_name(name).delete()

def change_product_name(cur_name: str, new_name: str) -> None:
    product = get_product_by_name(cur_name)
    product.product_name = new_name
    product.save()

def change_product_description(cur_descriotion: str, new_description: str) -> None:
    product = get_product_by_description(cur_descriotion)
    product.description = new_description
    product.save()

def change_product_prime_cost(name: str, prime_cost: int) -> None:
    product = get_product_by_name(name)
    product.prime_cost = prime_cost
    product.save()

def change_product_final_cost(name: str, final_cost: int) -> None:
    product = get_product_by_name(name)
    product.final_cost = final_cost
    product.save()

def change_product_info(name: str, description: str, quantity: int, prime_cost: int, final_cost: int) -> None:
    product = get_product_by_name(name)
    product.description = description
    product.quantity_in_stock = quantity
    product.prime_cost = prime_cost
    product.final_cost = final_cost
    product.save()

def remove_product_from_stock(name: str) -> None:
    product = get_product_by_name(name)
    cur_quantity = product.quantity_in_stock
    product.quantity_in_stock = cur_quantity - 1
    product.save()

def add_product_in_stock(name: str) -> None:
    product = get_product_by_name(name)
    cur_quantity = product.quantity_in_stock
    product.quantity_in_stock = cur_quantity + 1
    product.save()


