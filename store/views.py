from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from category.models import Category
from store.models import Product, Variation
from carts.models import CartItem
from carts.views import _get_cart_id

def store(request, category_slug=None):

    page_title = "Our Store"

    category = None
    products = Product.objects.filter(is_available=True).order_by('id')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    product_count = products.count()

    paginator = Paginator(products, 1)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'page_title': page_title,
        'products': paged_products,
        'product_count': product_count,
        'current_page': page
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    added_to_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), product__slug=product_slug).exists

    # variations = Variation.objects.filter(product=product)
    # for variation in variations:
    #     print(variation.variation_category, variation.variation_value)

    context = {
        'product': product,
        'added_to_cart': added_to_cart
    }

    return render(request, 'store/product_detail.html', context)


def search(request):

    page_title = "Search Results"

    if 'keyword' not in request.GET or request.GET.get('keyword') is None or request.GET.get('keyword') == '':
        return redirect('store')

    search_query = request.GET.get('keyword')

    products = Product.objects.order_by('created_date').filter(
        Q(description__icontains=search_query) | 
        Q(product_name__icontains=search_query)
    )

    product_count = products.count()

    context = {
        'page_title': page_title,
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)


