from django.urls import path

import cartapp.views as cartapp

app_name = 'cartapp'

urlpatterns = [
    path('add/<int:id_product>/', cartapp.cart_add, name='cart_add'),
    path('clear/', cartapp.cart_clear, name='cart_clear'),
    path('edit/<int:id>/<int:quantity>/', cartapp.cart_edit, name='cart_edit'),
    path('clear_position/<int:id_product>/', cartapp.cart_clear_position, name='cart_clear_position')
]
