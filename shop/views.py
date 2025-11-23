from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Product, Category, BlogPost
from django.conf import settings
from django.db.utils import OperationalError
from cart.views import _cart_id
from cart.models import CartItem
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from .models import ProductGallery

def home(request):
    products = Product.objects.all().filter(is_available=True)
    # Offer image in media (ensure MEDIA_URL is served in dev)
    offer_image = settings.MEDIA_URL + 'photos/products/offer.png'

    context = {
        'products' : products,
        'offer_image': offer_image,
    }
    return render(request, 'shop/index.html', context)


def shop(request, category_slug=None):
    categories = None
    products = None
    

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
        
    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
        
    
    for product in products:
        reviews = ReviewRating.objects.order_by('-updated_at').filter(product_id=product.id, status=True)

    context = {
        'category_slug': category_slug,
        'products' : paged_products,
        'products_count': products_count,
        
    }
    return render(request, 'shop/shop/shop.html', context)


def product_details(request, category_slug, product_details_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_details_slug)
        
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        return e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.order_by('-updated_at').filter(product_id=single_product.id, status=True)
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct':orderproduct,
        'reviews': reviews,
        'product_gallery':product_gallery,
    }
    return render(request, 'shop/shop/product_details.html', context)


def search(request):
    products_count = 0
    products = None
    paged_products = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword :
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
            
            products_count = products.count()
            
    
    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'shop/shop/search.html', context)



def review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you, your review updated!')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you, your review Posted!')
                return redirect(url)


def blog(request):
    """Render blog listing. Shows DB posts if present; otherwise the static teasers remain as fallback."""
    try:
        posts = BlogPost.objects.filter(is_published=True)
        # paginate
        page = request.GET.get('page')

        if posts.exists():
            paginator = Paginator(posts, 5)
            paged_posts = paginator.get_page(page)
            context = {
                'posts': paged_posts,
                'posts_count': posts.count(),
            }
        else:
            # No DB blog posts yet — build pseudo posts from Product images (shoes-first)
            from types import SimpleNamespace
            from django.db.models import Q

            # prefer products that mention 'shoe' in name or category
            products_qs = Product.objects.filter(Q(name__icontains='shoe') | Q(category__name__icontains='shoe'))
            if not products_qs.exists():
                products_qs = Product.objects.all()[:12]

            pseudo = []
            for p in products_qs[:10]:
                obj = SimpleNamespace()
                obj.title = f"{p.name} — Styling & Care"
                obj.excerpt = (p.description[:200] + '...') if p.description else 'Discover features, fit and styling tips for this product.'
                obj.content = p.description or obj.excerpt
                # provide a direct image URL attribute for the template
                obj.featured_image_url = p.image.url if p.image else None
                obj.author = 'E-SHOP'
                # use product creation date if available
                try:
                    obj.published_at = p.date_joined_for_format
                except Exception:
                    from django.utils import timezone
                    obj.published_at = timezone.now()
                # link to the product detail page
                obj.get_absolute_url = p.get_prodcut_details_url()
                pseudo.append(obj)

            paginator = Paginator(pseudo, 5)
            paged_posts = paginator.get_page(page)
            context = {
                'posts': paged_posts,
                'posts_count': len(pseudo),
            }
    except OperationalError:
        # Database table likely doesn't exist yet (migrations not applied).
        # Fall back to empty queryset so the template shows static teasers.
        context = {
            'posts': [],
            'posts_count': 0,
        }

    return render(request, 'blog.html', context)


def blog_detail(request, slug):
    try:
        post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    except OperationalError:
        # If the blog table doesn't exist, return a 404 page
        return render(request, 'blog_detail.html', {'post': None})

    return render(request, 'blog_detail.html', {'post': post})


def about(request):
    """Render an about page."""
    return render(request, 'about.html', {})


def contact(request):
    """Render a contact page."""
    return render(request, 'contact.html', {})
