from django.shortcuts import render, get_object_or_404
from category.models import Category
from store.models import Product
from carts.models import CartItem
from carts.views import _get_cart_id

def store(request, category_slug=None):

    category = None
    products = Product.objects.all().filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    added_to_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), product__slug=product_slug).exists

    context = {
        'product': product,
        'added_to_cart': added_to_cart
    }

    return render(request, 'store/product_detail.html', context)
