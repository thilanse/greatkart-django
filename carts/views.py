from django import contrib
from django.shortcuts import redirect, render
from .models import Cart, CartItem
from store.models import Product, Variation

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

    product_variations = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST.get(key)
        
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variations.append(variation)
            except:
                pass


    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_get_cart_id(request))
    
    cart.save()

    cart_items = CartItem.objects.filter(product=product, cart=cart)
    cart_items = [cart_item for cart_item in cart_items if list(cart_item.variations.all()) == product_variations]

    if len(cart_items) > 0:
        cart_item = cart_items[0]
        cart_item.quantity += 1
    else:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )

        if len(product_variations) > 0:
            for variation in product_variations:
                cart_item.variations.add(variation)
    
    cart_item.save()

    return redirect('cart')

def increment_quantity(request, cart_item_id):

    try:
        cart_item = CartItem.objects.get(id=cart_item_id)

        cart_item.quantity += 1
        cart_item.save()

    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

def decrement_quantity(request, cart_item_id):

    try:
        cart_item = CartItem.objects.get(id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

def remove_item(request, cart_item_id):

    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()

    except CartItem.DoesNotExist:
        pass

    return redirect('cart')
