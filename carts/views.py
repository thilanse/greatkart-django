from django import contrib
from django.shortcuts import redirect, render
from .models import Cart, CartItem
from store.models import Product

TAX_RATE = 0.02

def _get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def cart(request):

    cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), is_active=True)

    total_price = sum(item.total_price() for item in cart_items)
    total_tax = total_price * TAX_RATE

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_tax': total_tax,
        'grand_total': total_price + total_tax
    }

    return render(request, 'store/cart.html', context)


def add_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_get_cart_id(request))
    
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
    
    cart_item.save()

    return redirect('cart')

def decrement_quantity(request, product_id):

    cart_item = CartItem.objects.get(product__id=product_id, cart__cart_id=_get_cart_id(request))
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')

def remove_item(request, product_id):

    cart_item = CartItem.objects.get(product__id=product_id, cart__cart_id=_get_cart_id(request))
    cart_item.delete()

    return redirect('cart')
