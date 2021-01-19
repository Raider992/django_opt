from cartapp.models import Cart


def cart(request):
    cart_items = []

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

    return {
        'cart': cart_items
    }
