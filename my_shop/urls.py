from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mainapp import views as mainapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp_views.index, name='main'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('products/', include('mainapp.urls')),
    path('cart/', include('cartapp.urls', namespace='cart')),
    path('admin-staff/', include('adminapp.urls', namespace='admin_staff'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
