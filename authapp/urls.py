from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from authapp import views as authapp_views

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp_views.UserLoginView.as_view(), name='login'),
    path('logout', authapp_views.logout, name='logout'),
    path('register/', authapp_views.UserSignUpView.as_view(), name='register'),
    path('profile/', authapp_views.UserProfileView.as_view(), name='profile'),
    path('auth/', include('mainapp.urls', ))

]
