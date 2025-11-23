from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Variation, ReviewRating, ProductGallery
from .models import BlogPost
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category_image_preview']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def category_image_preview(self, obj):
        if obj.cat_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 8px;" />', obj.cat_image.url)
        return "No Image"
    category_image_preview.short_description = 'Image'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_image_preview', 'name', 'category', 'is_available', 'formatted_price', 'stock_status', 'new_badge', 'created']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_available', 'category', 'new']
    list_editable = ['is_available']
    readonly_fields = ['created', 'updated', 'date_joined_for_format', 'last_login_for_format']
    search_fields = ['name', 'description', 'category__name']
    inlines = [ProductGalleryInline]
    actions = ['make_available', 'make_unavailable', 'mark_as_new', 'clear_new_flag', 'apply_discount_percent']
    list_per_page = 25
    date_hierarchy = 'date_joined_for_format'
    ordering = ('-date_joined_for_format',)

    def make_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f"{updated} product(s) marked as available.")
    make_available.short_description = 'Mark selected products as available'

    def make_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f"{updated} product(s) marked as unavailable.")
    make_unavailable.short_description = 'Mark selected products as unavailable'

    def mark_as_new(self, request, queryset):
        updated = queryset.update(new=True)
        self.message_user(request, f"{updated} product(s) marked as NEW.")
    mark_as_new.short_description = 'Mark selected products as NEW'

    def clear_new_flag(self, request, queryset):
        updated = queryset.update(new=False)
        self.message_user(request, f"{updated} product(s) cleared NEW flag.")
    clear_new_flag.short_description = 'Clear NEW flag for selected products'

    def apply_discount_percent(self, request, queryset):
        """Apply a simple 10 percent discount to selected products (demo action)."""
        for p in queryset:
            p.discount = (p.price * 0.10)
            p.save()
        self.message_user(request, f"Applied 10 percent discount to {queryset.count()} product(s).")
    apply_discount_percent.short_description = 'Apply 10 percent discount to selected products'
    
    def product_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="border-radius: 8px;" />', obj.image.url)
        return "No Image"
    product_image_preview.short_description = 'Image'
    
    def formatted_price(self, obj):
        if obj.discount > 0:
            return format_html('<span style="color: #28a745; font-weight: bold;">${}</span>', obj.price - obj.discount)
        return format_html('<span style="color: #007bff; font-weight: bold;">${}</span>', obj.price)
    formatted_price.short_description = 'Price'
    
    def stock_status(self, obj):
        if obj.stock > 10:
            return format_html('<span style="color: #28a745;">✓ In Stock ({})</span>', obj.stock)
        elif obj.stock > 0:
            return format_html('<span style="color: #ffc107;">⚠ Low ({})</span>', obj.stock)
        return format_html('<span style="color: #dc3545;">✗ Out</span>')
    stock_status.short_description = 'Stock'
    
    def new_badge(self, obj):
        if obj.new:
            return format_html('<span style="background: #f5576c; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">NEW</span>')
        return "-"
    new_badge.short_description = 'New'

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value', 'is_active', 'status_badge']
    list_filter = ['product', 'variation_category', 'is_active']
    list_editable = ['is_active']
    search_fields = ['product__name', 'variation_value']
    list_per_page = 30
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">ACTIVE</span>')
        return format_html('<span style="background: #6c757d; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">INACTIVE</span>')
    status_badge.short_description = 'Status'

@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating_stars', 'status_badge']
    list_filter = ['rating', 'status']
    
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #ffc107;">{}</span>', stars)
    rating_stars.short_description = 'Rating'
    
    def status_badge(self, obj):
        if obj.status:
            return format_html('<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">APPROVED</span>')
        return format_html('<span style="background: #ffc107; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px;">PENDING</span>')
    status_badge.short_description = 'Status'

@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'product']
    list_filter = ['product']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="border-radius: 8px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'excerpt', 'content', 'author']
    list_filter = ['is_published', 'published_at']
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)
