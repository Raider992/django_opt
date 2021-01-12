from django.contrib import admin

from mainapp.models import ProductCategory, Product
from authapp.models import User

admin.site.register(ProductCategory)

admin.site.register(Product)

admin.site.register(User)