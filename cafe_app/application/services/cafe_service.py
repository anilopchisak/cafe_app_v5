from ..serializers import *
from .repository_service import *

class CafeService:
    # Customers
    def get_all_customers(self) -> CustomerSerializer:
        result = get_all_customers()
        return CustomerSerializer(result, many=True)

    def get_customer_by_name(self, name: str) -> Optional[CustomerSerializer]:
        result = get_customer_by_name(name)
        if result is not None:
            return CustomerSerializer(result)
        return result

    def get_customer_by_email(self, email: str) -> Optional[CustomerSerializer]:
        result = get_customer_by_email(email)
        print(result)
        if result is not None:
            return CustomerSerializer(result)
        return result

    def update_customer_name(self, customer: CustomerSerializer) -> None:
        customer_data = customer.data
        result = get_customer_by_email(customer_data.get('email'))
        return change_customer_name(result.customer_name, customer_data.get('customer_name'))

    def update_customer_email(self, customer: CustomerSerializer) -> None:
        customer_data = customer.data
        result = get_customer_by_name(customer_data.get('customer_name'))
        return change_customer_email(result.email, customer_data.get('email'))

    def add_customer(self, customer: CustomerSerializer) -> None:
        customer_data = customer.data
        # print(customer_data.get('customer_name'))
        return add_customer(name=customer_data.get('customer_name'),
                            email=customer_data.get('email'))

    def delete_customer_by_name(self, name: str) -> None:
        return delete_customer_by_name(name)

    def delete_customer_by_email(self, email: str) -> None:
        return delete_customer_by_email(email)

# Products
    def get_all_products(self) -> ProductSerializer:
        result = get_all_products()
        return ProductSerializer(result, many=True)

    def get_product_by_name(self, name: str) -> Optional[ProductSerializer]:
        result = get_product_by_name(name)
        if result is not None:
            return ProductSerializer(result)
        return result

    def update_product_info(self, product: ProductSerializer) -> None:
        product_data = product.data
        change_product_info(name=product_data.get('product_name'),
                           description=product_data.get('description'),
                           quantity=product_data.get('quantity_in_stock'),
                           prime_cost=product_data.get('prime_cost'),
                           final_cost=product_data.get('final_cost'))

    def add_product(self, product: ProductSerializer) -> None:
        product_data = product.data
        return add_product(name=product_data.get('product_name'),
                           description=product_data.get('description'),
                           quantity=product_data.get('quantity_in_stock'),
                           prime_cost=product_data.get('prime_cost'),
                           final_cost=product_data.get('final_cost'))

    def delete_product(self, name: str) -> None:
        return delete_product(name)


    # Orders
    def get_last_order_by_customer(self, name: str) -> Optional[OrderWithProductsSerializer]:
        result = get_last_order_by_customer_name(name)
        if result is not None:
            result_data = result.data
            products_in_order = get_products_from_order(result_data.id)
            products = []
            for product in products_in_order:
                products.append(product.product_name)
            customer_name = get_customer_by_order(result_data.id).customer_name
            payment_type = get_payment_type_by_order(result_data.id).payment_type
            return OrderWithProductsSerializer(id=result_data.id,
                                               customer=customer_name,
                                               products=products,
                                               full_cost=result_data.full_cost,
                                               date_time=result_data.date_time,
                                               payment_type=payment_type)
        return result

    def get_order_by_id(self, order_id: int) -> Optional[OrderWithProductsSerializer]:
        result = get_order_by_id(order_id)
        # print(result)
        if result is not None:
            # products_in_order = get_products_from_order(result.id)
            # products = []
            # for product in products_in_order:
            #     # print(product)
            #     products.append(product.product_name)
            # customer_name = (get_customer_by_order(result.id)).customer_name
            # payment_type = (get_payment_type_by_order(result.id)).payment_type
            # print(result.id, customer_name, products, result.order_cost, result.date_time, payment_type)
            # id = result.id
            # customer = customer_name
            # order_cost = result.order_cost
            # date_time = result.date_time
            # order = create_order_with_products_serializer(id, customer, products, order_cost, date_time, payment_type)
            order = OrderSerializer(result)
            # order = OrderWithProductsSerializer()
            # order_dict = {
            #     'res_id': result.id,
            #     }
            # result.id, customer_name, products, result.order_cost, result.date_time, payment_type)
            # order = OrderWithProductsSerializer(id=result.id, customer=customer_name, products=products,
            #                                     order_cost=result.order_cost, date_time=result.date_time,
            #                                     payment_type=payment_type)
            # order.create_order_with_products_serializer(print(order.data)
            # order = create_order_with_products_serializer(result.id, customer_name, products, result.order_cost, result.date_time, payment_type)
            return order
        return result

    def get_all_orders_by_customer(self, name: str) -> OrderSerializer:
        result = get_all_orders_by_customer_name(name)
        return OrderSerializer(result, many=True)

    def add_order(self, order: OrderWithProductsSerializer) -> None:
        order_data = order.data
        print(order_data)
        return add_order(customer_name=order_data.get('customer'), products=order_data.get('products'),
                         payment_type=order_data.get('payment_type'), date_time=order_data.get('date_time'))

    def delete_order_by_id(self, order: OrderSerializer) -> None:
        order_data = order.data
        return delete_order_by_id(order_data.id)

    def delete_all_orders_by_customer(self, name: str) -> None:
        return delete_all_orders_by_customer(name)


    # Payments
    def get_payment(self, order_id: int):
        result = get_payment(order_id)
        if result is not None:
            return PaymentSerializer(result)
        return None


    def update_payment(self, payment: PaymentSerializer) -> None:
        payment_data = payment.data
        # payment_type_id = get_payment_type_by_name(payment_data.payment_type).id
        return update_payment(payment_data.order_id, payment_data.payment_type)


    # Products in order ??
    def add_product_in_order(self, order_id: int, product_name: str) -> None:
        add_product_in_order(order_id, product_name)
        update_order_cost_by_id(order_id)

    # Payment types
    def get_all_payment_types(self) -> PaymentTypeSerializer:
        result = get_all_payment_types()
        return PaymentTypeSerializer(result, many=True)

    def add_payment_type(self, payment_type: PaymentTypeSerializer):
        payment_type_data = payment_type.data
        # TYPES.append(payment_type_data.get('payment_type'))
        return add_payment_type(payment_type_data.get('payment_type'))

    def delete_payment_type(self, payment_type: str):
        # TYPES.remove(payment_type)
        return delete_payment_type_by_name(payment_type)
