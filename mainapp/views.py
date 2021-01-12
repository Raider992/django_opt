from django.shortcuts import render
from django.utils import timezone
from mainapp.models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context = {
        'title': 'geek shop',

        'style_link': 'css/index.css',

        'date': timezone.now()

    }

    return render(request, 'mainapp/index.html', context)


def products(request, page=1, category_id=None):
    context = {
        'title': 'geek shop - каталог',
        'currency': 'руб.',
        'style_link': 'css/products.css',
        'categories': ProductCategory.objects.all(),
        'products': Product.objects.all()
    }

    if category_id:
        filtered_products = Product.objects.filter(category_id=category_id)
        context.update({'products': filtered_products})

    paginator = Paginator(context['products'], 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context.update({'products': products_paginator})

    return render(request, 'mainapp/products.html', context)
