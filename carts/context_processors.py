from .models import CartItem
from .views import _get_cart_id

def cart_item_count(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request))
    cart_item_count = sum(item.quantity for item in cart_items)
    return dict(cart_item_count=cart_item_count)