from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from adminapp import views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('users/', adminapp.UsersListView.as_view(), name='admin_users'),
    path('users/create', adminapp.UserCreateView.as_view(), name='admin_users_create'),
    path('users/update/<int:pk>', adminapp.UserUpdateView.as_view(), name='admin_users_update'),
    path('users/remove/<int:pk>', adminapp.UserRemoveView.as_view(), name='admin_users_remove'),
    path('users/restore/<int:pk>', adminapp.UserRestoreView.as_view(), name='admin_users_restore')

]
