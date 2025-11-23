from django import template
from django.db.models import Count
from shop.models import Product
try:
    from orders.models import Order
except Exception:
    Order = None
try:
    from accounts.models import Account
except Exception:
    Account = None

register = template.Library()


@register.inclusion_tag('admin/_admin_stats.html')
def get_admin_stats():
    """Return some basic site metrics for the admin dashboard."""
    total_products = Product.objects.count()
    available_products = Product.objects.filter(is_available=True).count()
    low_stock = Product.objects.filter(stock__lte=5).count()
    stats = {
        'total_products': total_products,
        'available_products': available_products,
        'low_stock': low_stock,
        'orders_count': Order.objects.count() if Order is not None else None,
        'users_count': Account.objects.count() if Account is not None else None,
    }
    return stats
