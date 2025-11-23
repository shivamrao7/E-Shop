from django.urls import path
from django.utils.regex_helper import normalize
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/<slug:category_slug>/', views.shop, name='categries'),
    path('shop/<slug:category_slug>/<slug:product_details_slug>/', views.product_details, name='product_details'),
    path('search/', views.search, name='search'),
    path('review/<int:product_id>/', views.review, name='review'),
    path('blog.html', views.blog, name='blog'),
    path('blog/', views.blog, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('about.html', views.about, name='about'),
    path('contact.html', views.contact, name='contact'),
]
