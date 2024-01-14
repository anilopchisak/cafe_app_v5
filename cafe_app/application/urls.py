from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from . import views

# Метаданные Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Zoo's Cafe",
      default_version='v1',
      description="Zoo's Cafe",
      terms_of_service="https://cafe_app.com",
      contact=openapi.Contact(email="lukporey1317@bk.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('zoo_cafe/order', views.PostOrder.as_view()),
    path('zoo_cafe/order/orders/<int:order_id>', views.GetOrder.as_view()),
    path('zoo_cafe/order/<str:customer_name>', views.GetDelAllOrders.as_view()),

    # path('zoo_cafe/order_detail/<int:id>', views.GetOrderById.as_view()),

    path('zoo_cafe/products_in_order/<int:order_id>&<str:product_name>', views.PutProductInOrder.as_view()),


    path('zoo_cafe/payment_type', views.GetPostPaymentType.as_view()),
    path('zoo_cafe/payment_type/<str:payment_type_name>', views.DelPaymentType.as_view()),

    path('zoo_cafe/product', views.GetPostPutProduct.as_view()),
    path('zoo_cafe/product/<str:product_name>', views.GetDelProduct.as_view()),

    path('zoo_cafe/customer', views.GetPostPutCustomer.as_view()),
    # path('zoo_cafe/customer/<str:customer_name>', views.GetDelCustomerByName.as_view()),
    path('zoo_cafe/customer/<str:email>', views.GetDelCustomerByEmail.as_view()),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]