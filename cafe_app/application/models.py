from django.db.models import *
# from django.utils import timezone

# Create your models here.


class Customer(Model):
    id = AutoField(primary_key=True)     # объявление первичного ключа с автоинкрементом
    customer_name = CharField('Name', null=False, max_length=20, unique=True)    # поле не может быть пустым (NULL)
    email = CharField('E-mail', null=False, max_length=30, unique=True)

    class Meta:
        """ Установка названия таблицы """
        db_table = 'customer'

    # @property
    # def temperature_c(self):
    #     """ Стандартные декораторы @property и @setter позволяют задать дополнительную
    #         бизнес-логику или проверку при присвоении атрибуту модели какого-либо значения """
    #     return self._temperature_c
    #
    # @temperature_c.setter
    # def temperature_c(self, temperature_c: float):
    #     """ При установке значения полю temperature_c будет автоматически рассчитано значение temperature_f """
    #     self.temperature_f = 32.0 + (temperature_c / 0.5556)
    #     self._temperature_c = temperature_c

    def __str__(self):
        """ Метод определяет строковое представление модели """
        return str({'id': self.id, 'name': self.customer_name, 'e-mail': self.email})


class Order(Model):
    id = AutoField(primary_key=True)
    customer_id = ForeignKey('Customer', verbose_name='Customer', null=False, on_delete=CASCADE)
    order_cost = DecimalField('Full cost', null=False, max_digits=7, decimal_places=2)
    date_time = DateTimeField('Date and time', null=False)

    class Meta:
        db_table = 'order'

    def __str__(self):
        return str({'id': self.id, 'customer_id': self.customer_id, 'order_cost': self.order_cost})


class Product(Model):
    id = AutoField(primary_key=True)
    product_name = TextField('Product', null=False, unique=True)
    description = TextField('Description', null=False, unique=True)
    quantity_in_stock = IntegerField('In stock', null=False)
    prime_cost = DecimalField('Prime cost', null=False, max_digits=5, decimal_places=2)
    final_cost = DecimalField('Full cost', null=False, max_digits=5, decimal_places=2)
    img = ImageField(upload_to='products_img', verbose_name='Фото продукта', blank=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return str({'product': self.product_name,
                    'in stock': self.quantity_in_stock, 'cost': self.final_cost})


class PaymentType(Model):
    TYPES = [
        ('SberPay', 'SberPay'),
        ('GooglePay', 'GooglePay'),
        ('Card', 'Card'),
        ('QR-code', 'QR-code'),
    ]
    id = AutoField(primary_key=True)
    payment_type = CharField('Payment type', null=False, max_length=10, choices=TYPES, unique=True)

    class Meta:
        db_table = 'payment_type'

    def __str__(self):
        return str({'id': self.id, 'payment_type': self.payment_type})


class Payment(Model):
    id = AutoField(primary_key=True)
    order_id = ForeignKey('Order', verbose_name='Order', null=False, on_delete=CASCADE)
    payment_type_id = ForeignKey('PaymentType', verbose_name='Payment type', null=False, on_delete=CASCADE)

    class Meta:
        db_table = 'Payment'

    def __str__(self):
        return str({'id': self.id, 'order_id': self.order_id, 'payment_type_id': self.payment_type_id})


class OrderProduct(Model):
    id = AutoField(primary_key=True)
    order_id = ForeignKey('Order', verbose_name='Order', null=False, on_delete=CASCADE)
    product_id = ForeignKey('Product', verbose_name='Product', null=False, on_delete=CASCADE)

    class Meta:
        db_table = 'order_product'

    def __str__(self):
        return str({'id': self.id, 'order_id': self.order_id, 'product_id': self.order_id})