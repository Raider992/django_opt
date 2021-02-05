from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from mainapp.models import Product
from cartapp.models import Cart


@login_required()
def cart_add(request, id_product=None):
    product = get_object_or_404(Product, id=id_product)
    carts = Cart.objects.filter(user=request.user, product=product)

    if not carts.exists():
        cart = Cart(user=request.user, product=product)
        cart.quantity += 1
        cart.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        cart = carts.first()
        cart.quantity += 1
        cart.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_edit(request, id, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        cart = Cart.objects.get(id=int(id))
        if quantity > 0:
            cart.quantity = quantity
            cart.save()
        else:
            cart.delete()
        carts = Cart.objects.filter(user=request.user)
        total_price = 0
        for cart in carts:
            total_price += cart.sum()

        context = {
            'carts': carts,
            'total_price': total_price
        }
        result = render_to_string('cartapp/cart.html', context)
        return JsonResponse({'result': result})


@login_required
def cart_clear_position(request, id_product=None):
    cart = Cart.objects.get(id=id_product)

    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_clear(request):
    cart = Cart.objects.all()
    cart.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
