from django.conf.urls import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='order'),
    path('create/', ordersapp.OrderCreate.as_view(), name='order_create'),
    path('update/<pk>', ordersapp.OrderUpdate.as_view(), name='order_update'),
    path('delete/<pk>', ordersapp.OrderDelete.as_view(), name='order_delete'),
    path('detail/<pk>', ordersapp.OrderDetail.as_view(), name='order_detail'),
    path('forming_complete/<pk>', ordersapp.order_forming_complete, name='order_forming_complete'),
    path('product/<pk>/price', ordersapp.get_product_price, name='get_product_price')
]
